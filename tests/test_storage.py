"""Tests for SQLite storage layer."""

from datetime import datetime, timedelta, timezone

import pytest

from src.ranking.rerank_llm import RankedPaper
from src.storage.sqlite import (
    get_connection,
    get_known_source_ids,
    get_last_run_timestamp,
    get_run_papers,
    load_paper,
    paper_exists,
    purge_old_data,
    save_papers,
    save_run,
)
from tests.conftest import make_paper


@pytest.fixture
def db_conn(tmp_path):
    """In-memory-like SQLite connection via temp file."""
    db_path = tmp_path / "test.db"
    conn = get_connection(db_path)
    yield conn
    conn.close()


class TestSavePapers:
    def test_save_new_papers(self, db_conn):
        papers = [make_paper("id-1", "Paper 1"), make_paper("id-2", "Paper 2")]
        inserted = save_papers(db_conn, papers)
        assert inserted == 2

    def test_save_duplicate_updates(self, db_conn):
        paper = make_paper("id-1", "Original Title")
        save_papers(db_conn, [paper])

        updated = make_paper("id-1", "Updated Title")
        inserted = save_papers(db_conn, [updated])
        assert inserted == 0  # no new inserts

        loaded = load_paper(db_conn, "id-1")
        assert loaded.title == "Updated Title"

    def test_save_empty_list(self, db_conn):
        inserted = save_papers(db_conn, [])
        assert inserted == 0


class TestPaperExists:
    def test_exists_after_save(self, db_conn):
        save_papers(db_conn, [make_paper("id-1")])
        assert paper_exists(db_conn, "id-1") is True

    def test_not_exists(self, db_conn):
        assert paper_exists(db_conn, "nonexistent") is False


class TestGetKnownSourceIds:
    def test_returns_known_ids(self, db_conn):
        save_papers(db_conn, [make_paper("id-1"), make_paper("id-2")])
        known = get_known_source_ids(db_conn, ["id-1", "id-2", "id-3"])
        assert known == {"id-1", "id-2"}

    def test_empty_input(self, db_conn):
        assert get_known_source_ids(db_conn, []) == set()


class TestLoadPaper:
    def test_load_existing(self, db_conn):
        original = make_paper("id-1", "Test Paper", authors=["Smith, John", "Doe, Jane"])
        save_papers(db_conn, [original])
        loaded = load_paper(db_conn, "id-1")
        assert loaded is not None
        assert loaded.title == "Test Paper"
        assert loaded.authors == ["Smith, John", "Doe, Jane"]
        assert loaded.source_type == "arxiv_api"

    def test_load_nonexistent(self, db_conn):
        assert load_paper(db_conn, "nonexistent") is None


class TestRunOperations:
    def test_save_and_load_run(self, db_conn):
        paper = make_paper("id-1", "Test")
        save_papers(db_conn, [paper])

        ranked = [RankedPaper(paper=paper, relevance_score=8, reasoning="Good match", summary="Summary here")]
        run_id = save_run(db_conn, ranked, total_fetched=10, config_snapshot={"key": "value"})
        assert run_id is not None

        loaded = get_run_papers(db_conn, run_id)
        assert len(loaded) == 1
        assert loaded[0].relevance_score == 8
        assert loaded[0].reasoning == "Good match"

    def test_last_run_timestamp(self, db_conn):
        assert get_last_run_timestamp(db_conn) is None

        paper = make_paper("id-1")
        save_papers(db_conn, [paper])
        ranked = [RankedPaper(paper=paper, relevance_score=5, reasoning="Ok", summary="Sum")]
        save_run(db_conn, ranked)

        ts = get_last_run_timestamp(db_conn)
        assert ts is not None

    def test_multiple_runs(self, db_conn):
        p1 = make_paper("id-1")
        p2 = make_paper("id-2")
        save_papers(db_conn, [p1, p2])

        rp1 = RankedPaper(paper=p1, relevance_score=8, reasoning="R1", summary="S1")
        rp2 = RankedPaper(paper=p2, relevance_score=6, reasoning="R2", summary="S2")

        run1 = save_run(db_conn, [rp1], total_fetched=5)
        run2 = save_run(db_conn, [rp2], total_fetched=3)

        assert len(get_run_papers(db_conn, run1)) == 1
        assert len(get_run_papers(db_conn, run2)) == 1


def _insert_run_at(db_conn, papers, timestamp):
    """Helper: save a run with a specific timestamp (bypassing save_run's auto-now)."""
    cursor = db_conn.execute(
        "INSERT INTO runs (run_timestamp, total_fetched, total_ranked, config_snapshot) VALUES (?, ?, ?, ?)",
        (timestamp.isoformat(), len(papers), len(papers), "{}"),
    )
    run_id = cursor.lastrowid
    for rp in papers:
        db_conn.execute(
            "INSERT INTO run_papers (run_id, source_id, relevance_score, reasoning, summary) VALUES (?, ?, ?, ?, ?)",
            (run_id, rp.paper.source_id, rp.relevance_score, rp.reasoning, rp.summary),
        )
    db_conn.commit()
    return run_id


def _set_paper_first_seen(db_conn, source_id, timestamp):
    """Helper: override first_seen for a paper."""
    db_conn.execute(
        "UPDATE papers SET first_seen = ? WHERE source_id = ?",
        (timestamp.isoformat(), source_id),
    )
    db_conn.commit()


class TestPurgeOldData:
    def test_dry_run_does_not_delete(self, db_conn):
        old_time = datetime.now(timezone.utc) - timedelta(days=100)
        p = make_paper("id-1")
        save_papers(db_conn, [p])
        _set_paper_first_seen(db_conn, "id-1", old_time)
        rp = RankedPaper(paper=p, relevance_score=7, reasoning="R", summary="S")
        _insert_run_at(db_conn, [rp], old_time)

        counts = purge_old_data(db_conn, older_than_days=90, dry_run=True)
        assert counts["runs"] == 1
        assert counts["run_papers"] == 1
        assert counts["orphaned_papers"] == 1

        # Data should still exist
        assert paper_exists(db_conn, "id-1")
        assert get_last_run_timestamp(db_conn) is not None

    def test_purge_old_run_and_orphaned_paper(self, db_conn):
        old_time = datetime.now(timezone.utc) - timedelta(days=100)
        p = make_paper("id-1")
        save_papers(db_conn, [p])
        _set_paper_first_seen(db_conn, "id-1", old_time)
        rp = RankedPaper(paper=p, relevance_score=7, reasoning="R", summary="S")
        _insert_run_at(db_conn, [rp], old_time)

        counts = purge_old_data(db_conn, older_than_days=90)
        assert counts["runs"] == 1
        assert counts["run_papers"] == 1
        assert counts["orphaned_papers"] == 1

        # Data should be gone
        assert not paper_exists(db_conn, "id-1")
        assert get_last_run_timestamp(db_conn) is None

    def test_keeps_recent_runs(self, db_conn):
        old_time = datetime.now(timezone.utc) - timedelta(days=100)
        recent_time = datetime.now(timezone.utc) - timedelta(days=10)

        p1 = make_paper("id-old")
        p2 = make_paper("id-recent")
        save_papers(db_conn, [p1, p2])
        _set_paper_first_seen(db_conn, "id-old", old_time)
        _set_paper_first_seen(db_conn, "id-recent", recent_time)

        rp_old = RankedPaper(paper=p1, relevance_score=5, reasoning="R", summary="S")
        rp_recent = RankedPaper(paper=p2, relevance_score=8, reasoning="R", summary="S")
        _insert_run_at(db_conn, [rp_old], old_time)
        _insert_run_at(db_conn, [rp_recent], recent_time)

        counts = purge_old_data(db_conn, older_than_days=90)
        assert counts["runs"] == 1
        assert not paper_exists(db_conn, "id-old")
        assert paper_exists(db_conn, "id-recent")

    def test_shared_paper_not_deleted(self, db_conn):
        """A paper referenced by both an old and recent run should not be deleted."""
        old_time = datetime.now(timezone.utc) - timedelta(days=100)
        recent_time = datetime.now(timezone.utc) - timedelta(days=10)

        p = make_paper("id-shared")
        save_papers(db_conn, [p])
        _set_paper_first_seen(db_conn, "id-shared", old_time)

        rp = RankedPaper(paper=p, relevance_score=7, reasoning="R", summary="S")
        _insert_run_at(db_conn, [rp], old_time)
        _insert_run_at(db_conn, [rp], recent_time)

        counts = purge_old_data(db_conn, older_than_days=90)
        assert counts["runs"] == 1  # only old run deleted
        assert paper_exists(db_conn, "id-shared")  # still referenced by recent run

    def test_nothing_to_purge(self, db_conn):
        recent_time = datetime.now(timezone.utc) - timedelta(days=5)
        p = make_paper("id-1")
        save_papers(db_conn, [p])
        rp = RankedPaper(paper=p, relevance_score=7, reasoning="R", summary="S")
        _insert_run_at(db_conn, [rp], recent_time)

        counts = purge_old_data(db_conn, older_than_days=90)
        assert counts["runs"] == 0
        assert counts["run_papers"] == 0
        assert counts["orphaned_papers"] == 0
        assert paper_exists(db_conn, "id-1")
