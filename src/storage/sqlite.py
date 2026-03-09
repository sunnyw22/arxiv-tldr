"""SQLite storage for paper cache, deduplication, and run history.

Schema:
- papers: cached paper metadata, keyed by source_id
- runs: digest run history (timestamp, config snapshot)
- run_papers: papers included in each run with their scores and summaries
"""

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from src.core.models import Paper
from src.ranking.rerank_llm import RankedPaper

DEFAULT_DB_PATH = "data/research_radar.db"


def get_connection(db_path: str | Path = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Open a connection and ensure tables exist."""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    _init_tables(conn)
    return conn


def _init_tables(conn: sqlite3.Connection) -> None:
    """Create tables if they don't exist."""
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS papers (
            source_id       TEXT PRIMARY KEY,
            title           TEXT NOT NULL,
            authors         TEXT NOT NULL,       -- JSON list
            abstract        TEXT NOT NULL,
            categories      TEXT NOT NULL,       -- JSON list
            primary_category TEXT NOT NULL,
            submitted_date  TEXT NOT NULL,       -- ISO 8601
            updated_date    TEXT,                -- ISO 8601 or NULL
            source_url      TEXT NOT NULL,
            pdf_url         TEXT NOT NULL,
            source_type     TEXT NOT NULL,
            raw_metadata    TEXT NOT NULL,       -- JSON blob
            first_seen      TEXT NOT NULL        -- when we first fetched this paper
        );

        CREATE TABLE IF NOT EXISTS runs (
            run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
            run_timestamp   TEXT NOT NULL,       -- ISO 8601
            total_fetched   INTEGER NOT NULL DEFAULT 0,
            total_ranked    INTEGER NOT NULL DEFAULT 0,
            config_snapshot TEXT NOT NULL        -- JSON blob of config used
        );

        CREATE TABLE IF NOT EXISTS run_papers (
            run_id            INTEGER NOT NULL,
            source_id         TEXT NOT NULL,
            relevance_score   INTEGER NOT NULL,
            reasoning         TEXT NOT NULL,
            summary           TEXT NOT NULL,
            abstract_takeaway TEXT NOT NULL DEFAULT '',
            why_relevant      TEXT NOT NULL DEFAULT '',
            PRIMARY KEY (run_id, source_id),
            FOREIGN KEY (run_id) REFERENCES runs(run_id),
            FOREIGN KEY (source_id) REFERENCES papers(source_id)
        );

        CREATE TABLE IF NOT EXISTS source_checkpoints (
            source_name     TEXT PRIMARY KEY,
            last_fetched    TEXT NOT NULL,       -- ISO 8601 timestamp
            papers_fetched  INTEGER NOT NULL DEFAULT 0
        );
    """)
    # Migrate existing DBs: add new columns if missing
    _migrate_run_papers(conn)


def _migrate_run_papers(conn: sqlite3.Connection) -> None:
    """Add abstract_takeaway and why_relevant columns to run_papers if missing."""
    cursor = conn.execute("PRAGMA table_info(run_papers)")
    columns = {row[1] for row in cursor.fetchall()}
    if "abstract_takeaway" not in columns:
        conn.execute("ALTER TABLE run_papers ADD COLUMN abstract_takeaway TEXT NOT NULL DEFAULT ''")
    if "why_relevant" not in columns:
        conn.execute("ALTER TABLE run_papers ADD COLUMN why_relevant TEXT NOT NULL DEFAULT ''")


# --- Paper operations ---

def save_papers(conn: sqlite3.Connection, papers: list[Paper]) -> int:
    """Insert or update papers. Returns count of newly inserted papers."""
    inserted = 0
    now = datetime.now(timezone.utc).isoformat()
    for p in papers:
        try:
            conn.execute(
                """INSERT INTO papers
                   (source_id, title, authors, abstract, categories,
                    primary_category, submitted_date, updated_date,
                    source_url, pdf_url, source_type, raw_metadata, first_seen)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    p.source_id,
                    p.title,
                    json.dumps(p.authors),
                    p.abstract,
                    json.dumps(p.categories),
                    p.primary_category,
                    p.submitted_date.isoformat(),
                    p.updated_date.isoformat() if p.updated_date else None,
                    p.source_url,
                    p.pdf_url,
                    p.source_type,
                    json.dumps(p.raw_metadata),
                    now,
                ),
            )
            inserted += 1
        except sqlite3.IntegrityError:
            # Already exists — update metadata in case it changed
            conn.execute(
                """UPDATE papers SET title=?, authors=?, abstract=?, categories=?,
                   primary_category=?, submitted_date=?, updated_date=?,
                   source_url=?, pdf_url=?, raw_metadata=?
                   WHERE source_id=?""",
                (
                    p.title,
                    json.dumps(p.authors),
                    p.abstract,
                    json.dumps(p.categories),
                    p.primary_category,
                    p.submitted_date.isoformat(),
                    p.updated_date.isoformat() if p.updated_date else None,
                    p.source_url,
                    p.pdf_url,
                    json.dumps(p.raw_metadata),
                    p.source_id,
                ),
            )
    conn.commit()
    return inserted


def paper_exists(conn: sqlite3.Connection, source_id: str) -> bool:
    """Check if a paper is already in the database."""
    row = conn.execute(
        "SELECT 1 FROM papers WHERE source_id = ?", (source_id,)
    ).fetchone()
    return row is not None


def get_known_source_ids(conn: sqlite3.Connection, source_ids: list[str]) -> set[str]:
    """Return the subset of source_ids that already exist in the database.

    Uses a single query for efficiency.
    """
    if not source_ids:
        return set()
    placeholders = ",".join("?" for _ in source_ids)
    rows = conn.execute(
        f"SELECT source_id FROM papers WHERE source_id IN ({placeholders})",
        source_ids,
    ).fetchall()
    return {row["source_id"] for row in rows}


def load_paper(conn: sqlite3.Connection, source_id: str) -> Paper | None:
    """Load a single paper from the database."""
    row = conn.execute(
        "SELECT * FROM papers WHERE source_id = ?", (source_id,)
    ).fetchone()
    if not row:
        return None
    return _row_to_paper(row)


# --- Run operations ---

def save_run(
    conn: sqlite3.Connection,
    ranked_papers: list[RankedPaper],
    total_fetched: int = 0,
    config_snapshot: dict | None = None,
) -> int:
    """Save a digest run and its ranked papers. Returns the run_id."""
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.execute(
        """INSERT INTO runs (run_timestamp, total_fetched, total_ranked, config_snapshot)
           VALUES (?, ?, ?, ?)""",
        (now, total_fetched, len(ranked_papers), json.dumps(config_snapshot or {})),
    )
    run_id = cursor.lastrowid

    for rp in ranked_papers:
        conn.execute(
            """INSERT OR REPLACE INTO run_papers
               (run_id, source_id, relevance_score, reasoning, summary,
                abstract_takeaway, why_relevant)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (run_id, rp.paper.source_id, rp.relevance_score, rp.reasoning, rp.summary,
             rp.abstract_takeaway, rp.why_relevant),
        )

    conn.commit()
    return run_id


def get_last_run_timestamp(conn: sqlite3.Connection) -> datetime | None:
    """Get the timestamp of the most recent run, or None if no runs exist."""
    row = conn.execute(
        "SELECT run_timestamp FROM runs ORDER BY run_id DESC LIMIT 1"
    ).fetchone()
    if not row:
        return None
    return datetime.fromisoformat(row["run_timestamp"])


def get_run_papers(conn: sqlite3.Connection, run_id: int) -> list[RankedPaper]:
    """Load ranked papers for a specific run."""
    rows = conn.execute(
        """SELECT rp.*, p.* FROM run_papers rp
           JOIN papers p ON rp.source_id = p.source_id
           WHERE rp.run_id = ?
           ORDER BY rp.relevance_score DESC""",
        (run_id,),
    ).fetchall()

    results = []
    for row in rows:
        paper = _row_to_paper(row)
        results.append(RankedPaper(
            paper=paper,
            relevance_score=row["relevance_score"],
            reasoning=row["reasoning"],
            summary=row["summary"],
            abstract_takeaway=row["abstract_takeaway"] if "abstract_takeaway" in row.keys() else "",
            why_relevant=row["why_relevant"] if "why_relevant" in row.keys() else "",
        ))
    return results


# --- Helpers ---

def save_source_checkpoint(
    conn: sqlite3.Connection,
    source_name: str,
    timestamp: datetime,
    count: int,
) -> None:
    """Save or update a source checkpoint (last fetch time and count)."""
    conn.execute(
        """INSERT INTO source_checkpoints (source_name, last_fetched, papers_fetched)
           VALUES (?, ?, ?)
           ON CONFLICT(source_name) DO UPDATE SET
               last_fetched = excluded.last_fetched,
               papers_fetched = excluded.papers_fetched""",
        (source_name, timestamp.isoformat(), count),
    )
    conn.commit()


def get_source_checkpoint(conn: sqlite3.Connection, source_name: str) -> datetime | None:
    """Get the last fetch timestamp for a source, or None if never fetched."""
    row = conn.execute(
        "SELECT last_fetched FROM source_checkpoints WHERE source_name = ?",
        (source_name,),
    ).fetchone()
    if not row:
        return None
    return datetime.fromisoformat(row["last_fetched"])


def purge_old_data(
    conn: sqlite3.Connection,
    older_than_days: int,
    dry_run: bool = False,
) -> dict[str, int]:
    """Delete runs older than the given number of days, plus orphaned papers.

    Deletes: old runs → their run_papers → papers no longer in any run.
    Returns counts of deleted rows per table.
    """
    from datetime import timedelta

    cutoff = (datetime.now(timezone.utc) - timedelta(days=older_than_days)).isoformat()

    # 1. Identify old runs
    old_run_ids = [
        row[0]
        for row in conn.execute(
            "SELECT run_id FROM runs WHERE run_timestamp < ?", (cutoff,)
        ).fetchall()
    ]

    # 2. Count run_papers that will be deleted
    run_papers_count = 0
    if old_run_ids:
        placeholders = ",".join("?" for _ in old_run_ids)
        run_papers_count = conn.execute(
            f"SELECT COUNT(*) FROM run_papers WHERE run_id IN ({placeholders})",
            old_run_ids,
        ).fetchone()[0]

    # 3. Count papers that will become orphaned after purge
    # A paper is orphaned if it's not referenced by any run that survives
    orphan_count = conn.execute(
        """SELECT COUNT(*) FROM papers WHERE source_id NOT IN (
               SELECT DISTINCT source_id FROM run_papers
               WHERE run_id NOT IN (
                   SELECT run_id FROM runs WHERE run_timestamp < ?
               )
           ) AND first_seen < ?""",
        (cutoff, cutoff),
    ).fetchone()[0]

    counts = {
        "runs": len(old_run_ids),
        "run_papers": run_papers_count,
        "orphaned_papers": orphan_count,
    }

    if dry_run or (not old_run_ids and orphan_count == 0):
        return counts

    # Delete in FK-safe order: run_papers → runs → orphaned papers
    if old_run_ids:
        placeholders = ",".join("?" for _ in old_run_ids)
        conn.execute(
            f"DELETE FROM run_papers WHERE run_id IN ({placeholders})",
            old_run_ids,
        )
        conn.execute(
            f"DELETE FROM runs WHERE run_id IN ({placeholders})",
            old_run_ids,
        )

    # Delete papers not referenced by any remaining run and old enough
    conn.execute(
        """DELETE FROM papers
           WHERE source_id NOT IN (SELECT DISTINCT source_id FROM run_papers)
           AND first_seen < ?""",
        (cutoff,),
    )

    conn.commit()
    return counts


def _row_to_paper(row: sqlite3.Row) -> Paper:
    """Convert a database row to a Paper object."""
    return Paper(
        source_id=row["source_id"],
        title=row["title"],
        authors=json.loads(row["authors"]),
        abstract=row["abstract"],
        categories=json.loads(row["categories"]),
        primary_category=row["primary_category"],
        submitted_date=datetime.fromisoformat(row["submitted_date"]),
        source_url=row["source_url"],
        pdf_url=row["pdf_url"],
        source_type=row["source_type"],
        updated_date=datetime.fromisoformat(row["updated_date"]) if row["updated_date"] else None,
        raw_metadata=json.loads(row["raw_metadata"]),
    )
