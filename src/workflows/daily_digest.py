"""Daily digest workflow — end-to-end orchestration.

Fetches papers from configured sources, deduplicates, ranks via LLM,
generates reports, and persists results to SQLite.
"""

import hashlib
import json
import re
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from src.core.config import AppConfig
from src.core.models import Paper
from src.profiles.schema import UserProfile
from src.ranking.keyword import score_paper
from src.ranking.rerank_llm import RankedPaper, rerank_and_summarize
from src.ranking.synonym import expand_keywords
from src.reports import timestamped_filename
from src.reports.html import generate_html_report
from src.reports.markdown import generate_markdown_report
from src.sources.arxiv_api import ArxivAPI
from src.sources.inspire import InspireAPI
from src.storage.sqlite import (
    get_connection,
    get_last_run_timestamp,
    get_run_papers,
    save_papers,
    save_run,
    save_source_checkpoint,
)
from src.summarization.llm_client import reset_token_usage, token_usage


def profile_hash(profile: UserProfile) -> str:
    """Deterministic hash of profile fields that affect ranking."""
    key_fields = {
        "topic_interests": sorted(profile.topic_interests),
        "project_context": profile.project_context.strip(),
        "expertise_level": profile.expertise_level.strip(),
    }
    raw = json.dumps(key_fields, sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def run_daily_digest(
    config: AppConfig,
    db_path: str | Path = "data/research_radar.db",
    since_date: datetime | None = None,
    until_date: datetime | None = None,
) -> dict:
    """Run the full daily digest pipeline.

    Args:
        config: Application configuration.
        db_path: Path to SQLite database.
        since_date: If provided, filter papers with submitted_date >= since_date.
        until_date: If provided, filter papers with submitted_date <= until_date.

    Returns:
        Dict with keys: ranked_papers, md_path, html_path, run_id, stats
    """
    conn = get_connection(db_path)
    reset_token_usage()

    # Initialize pipeline stats
    pipeline_stats = {
        "arxiv_fetched": 0,
        "inspire_fetched": 0,
    }

    # --- 1. Fetch papers from sources ---
    all_papers, source_counts = _fetch_papers(config)
    pipeline_stats["arxiv_fetched"] = source_counts.get("arxiv", 0)
    pipeline_stats["inspire_fetched"] = source_counts.get("inspire", 0)
    total_fetched = len(all_papers)
    pipeline_stats["total_fetched"] = total_fetched
    print(f"Fetched {total_fetched} papers from sources")

    # Save source checkpoints
    now_ts = datetime.now(timezone.utc)
    if source_counts.get("arxiv", 0) > 0:
        save_source_checkpoint(conn, "arxiv", now_ts, source_counts["arxiv"])
    if source_counts.get("inspire", 0) > 0:
        save_source_checkpoint(conn, "inspire", now_ts, source_counts["inspire"])

    if not all_papers:
        print("No papers fetched. Check your source configuration.")
        conn.close()
        return {"ranked_papers": [], "stats": {"total_fetched": 0}}

    # --- 1b. Apply date window filter ---
    if since_date or until_date:
        all_papers = _filter_by_date(all_papers, since_date, until_date)
        print(f"After date filter: {len(all_papers)} papers")
        if not all_papers:
            print("No papers in the specified date range.")
            conn.close()
            return {"ranked_papers": [], "stats": {"total_fetched": total_fetched}}

    # Build digest window description
    if since_date or until_date:
        since_str = since_date.strftime("%Y-%m-%d") if since_date else "earliest"
        until_str = until_date.strftime("%Y-%m-%d") if until_date else "latest"
        pipeline_stats["digest_window"] = f"Papers from {since_str} to {until_str}"
    else:
        pipeline_stats["digest_window"] = f"Fetched {total_fetched} most recent papers"

    # --- 2. Cross-source dedup ---
    unique = _dedup_papers(all_papers)
    pipeline_stats["unique_papers"] = len(unique)
    print(f"After dedup: {len(unique)} unique papers")

    # --- 3. Save all papers to DB ---
    new_count = save_papers(conn, unique)
    print(f"Papers: {new_count} new, {len(unique) - new_count} already known")

    # --- 4. Check profile change ---
    current_hash = profile_hash(config.profile)
    previous_ranked = _load_previous_scores(conn, current_hash, unique)

    # Separate papers into already-scored and needs-scoring
    already_scored_ids = {rp.paper.source_id for rp in previous_ranked}
    needs_scoring = [p for p in unique if p.source_id not in already_scored_ids]

    if previous_ranked:
        print(f"Reusing {len(previous_ranked)} previously scored papers (same profile)")
    print(f"Papers needing LLM scoring: {len(needs_scoring)}")

    # --- 5. Rank new papers ---
    newly_ranked = []
    expanded_keywords: list[str] = []
    keyword_passed = 0
    keyword_rejected = 0
    if needs_scoring:
        newly_ranked, expanded_keywords, keyword_passed, keyword_rejected = _rank_papers(
            needs_scoring, config
        )
        print(f"LLM ranked {len(newly_ranked)} new papers")

    pipeline_stats["keyword_passed"] = keyword_passed
    pipeline_stats["keyword_rejected"] = keyword_rejected
    pipeline_stats["llm_scored"] = len(newly_ranked)
    pipeline_stats["expanded_keywords"] = expanded_keywords

    # --- 6. Merge and sort ---
    all_ranked = previous_ranked + newly_ranked
    all_ranked.sort(key=lambda r: r.relevance_score, reverse=True)

    # Apply top_n with tie-inclusive cutoff
    top_n = config.summary.max_papers
    if len(all_ranked) > top_n:
        cutoff_score = all_ranked[top_n - 1].relevance_score
        all_ranked = [r for r in all_ranked if r.relevance_score >= cutoff_score]

    pipeline_stats["final_count"] = len(all_ranked)
    print(f"Final digest: {len(all_ranked)} papers")

    # --- 7. Save run to DB ---
    config_snapshot = {
        "profile_hash": current_hash,
        "profile": asdict(config.profile),
        "sources": asdict(config.sources),
        "llm_model": config.llm.model,
    }
    run_id = save_run(conn, all_ranked, total_fetched=total_fetched, config_snapshot=config_snapshot)

    # --- 8. Generate reports ---
    md_path, html_path = _generate_reports(
        all_ranked, config, total_fetched,
        expanded_keywords=expanded_keywords,
        pipeline_stats=pipeline_stats,
    )

    conn.close()

    stats = {
        "total_fetched": total_fetched,
        "unique_papers": pipeline_stats["unique_papers"],
        "new_papers": new_count,
        "reused_scores": len(previous_ranked),
        "newly_ranked": len(newly_ranked),
        "final_count": pipeline_stats["final_count"],
        "keyword_passed": keyword_passed,
        "keyword_rejected": keyword_rejected,
        "llm_scored": len(newly_ranked),
        "run_id": run_id,
        "token_usage": token_usage.report(),
    }
    print(f"\n{token_usage.report()}")

    return {
        "ranked_papers": all_ranked,
        "md_path": md_path,
        "html_path": html_path,
        "run_id": run_id,
        "stats": stats,
    }


def _filter_by_date(
    papers: list[Paper],
    since_date: datetime | None,
    until_date: datetime | None,
) -> list[Paper]:
    """Filter papers by submitted_date within [since_date, until_date]."""
    filtered = papers
    if since_date:
        filtered = [p for p in filtered if p.submitted_date >= since_date]
    if until_date:
        filtered = [p for p in filtered if p.submitted_date <= until_date]
    return filtered


def _fetch_papers(config: AppConfig) -> tuple[list[Paper], dict[str, int]]:
    """Fetch papers from all enabled sources.

    Returns:
        Tuple of (papers, source_counts) where source_counts maps source name to count.
    """
    papers = []
    source_counts: dict[str, int] = {}

    if config.sources.arxiv.enabled and config.sources.arxiv.categories:
        print("Fetching from arXiv API...")
        try:
            arxiv = ArxivAPI()
            arxiv_papers = arxiv.fetch(
                categories=config.sources.arxiv.categories,
                max_results=config.sources.arxiv.max_results,
            )
            print(f"  arXiv: {len(arxiv_papers)} papers")
            source_counts["arxiv"] = len(arxiv_papers)
            papers.extend(arxiv_papers)
        except Exception as e:
            print(f"  arXiv fetch failed: {e}")

    if config.sources.inspire.enabled:
        keywords = config.sources.inspire.keywords
        subject_codes = config.sources.inspire.subject_codes
        if keywords or subject_codes:
            print("Fetching from INSPIRE...")
            try:
                inspire = InspireAPI()
                inspire_papers = inspire.fetch(
                    keywords=keywords,
                    subject_codes=subject_codes,
                    max_results=config.sources.inspire.max_results,
                )
                print(f"  INSPIRE: {len(inspire_papers)} papers")
                source_counts["inspire"] = len(inspire_papers)
                papers.extend(inspire_papers)
            except Exception as e:
                print(f"  INSPIRE fetch failed: {e}")

    return papers, source_counts


def _normalize_title(title: str) -> str:
    """Normalize a title for fuzzy dedup: lowercase, strip, collapse spaces."""
    return re.sub(r"\s+", " ", title.lower().strip())


def _first_author_last_name(authors: list[str]) -> str:
    """Extract the last name of the first author.

    Handles both "Last, First" and "First Last" formats.
    Returns lowercased last name for comparison.
    """
    if not authors:
        return ""
    first_author = authors[0].strip()
    if "," in first_author:
        # "Last, First" format
        return first_author.split(",")[0].strip().lower()
    # "First Last" format
    parts = first_author.split()
    return parts[-1].strip().lower() if parts else ""


def _dedup_papers(papers: list[Paper]) -> list[Paper]:
    """Deduplicate papers across sources.

    Uses tiered matching (cheap to expensive):
      1. arXiv ID (version-stripped)
      2. DOI (exact match)
      3. source_id (exact match)
      4. Normalized title + first author last name + year
    First occurrence wins when duplicates are found.

    Note: Tier 4 could theoretically false-positive if two genuinely different
    papers share the same title, first-author last name, and year (e.g. generic
    titles like "Review of Particle Physics" by common last names). No real case
    found in practice. If reported, add second-author or abstract similarity check.
    """
    seen_arxiv: set[str] = set()
    seen_doi: set[str] = set()
    seen_source: set[str] = set()
    seen_title_author_year: set[str] = set()
    unique: list[Paper] = []

    for p in papers:
        # --- Tier 1: arXiv ID (version-stripped) ---
        arxiv_id = None
        if p.source_type in ("arxiv", "arxiv_rss", "arxiv_api"):
            arxiv_id = p.source_id.split("v")[0]
        elif p.raw_metadata.get("arxiv_id"):
            arxiv_id = p.raw_metadata["arxiv_id"].split("v")[0]

        if arxiv_id:
            if arxiv_id in seen_arxiv:
                continue
            seen_arxiv.add(arxiv_id)
            # Also register DOI/source_id/title so later papers can't bypass
            doi = p.raw_metadata.get("doi", "").strip().lower()
            if doi:
                seen_doi.add(doi)
            seen_source.add(p.source_id)
            tay = _title_author_year_key(p)
            if tay:
                seen_title_author_year.add(tay)
            unique.append(p)
            continue

        # --- Tier 2: DOI (exact match) ---
        doi = p.raw_metadata.get("doi", "").strip().lower()
        if doi:
            if doi in seen_doi:
                continue
            seen_doi.add(doi)
            seen_source.add(p.source_id)
            tay = _title_author_year_key(p)
            if tay:
                seen_title_author_year.add(tay)
            unique.append(p)
            continue

        # --- Tier 3: source_id (exact match) ---
        if p.source_id in seen_source:
            continue
        seen_source.add(p.source_id)

        # --- Tier 4: Normalized title + first author last name + year ---
        tay = _title_author_year_key(p)
        if tay:
            if tay in seen_title_author_year:
                continue
            seen_title_author_year.add(tay)

        unique.append(p)

    return unique


def _title_author_year_key(paper: Paper) -> str | None:
    """Build a title+author+year dedup key, or None if insufficient data."""
    title = _normalize_title(paper.title)
    last_name = _first_author_last_name(paper.authors)
    if not title or not last_name:
        return None
    year = str(paper.submitted_date.year)
    return f"{title}|{last_name}|{year}"


def _load_previous_scores(
    conn,
    current_hash: str,
    papers: list[Paper],
) -> list[RankedPaper]:
    """Load scores from the most recent run IF the profile hasn't changed."""
    last_ts = get_last_run_timestamp(conn)
    if last_ts is None:
        return []

    # Get the most recent run's config
    row = conn.execute(
        "SELECT run_id, config_snapshot FROM runs ORDER BY run_id DESC LIMIT 1"
    ).fetchone()
    if not row:
        return []

    try:
        snapshot = json.loads(row["config_snapshot"])
    except (json.JSONDecodeError, TypeError):
        return []

    if snapshot.get("profile_hash") != current_hash:
        print("Profile changed since last run — re-ranking all papers")
        return []

    # Load previous scores and filter to papers in the current fetch
    current_ids = {p.source_id for p in papers}
    previous = get_run_papers(conn, row["run_id"])
    return [rp for rp in previous if rp.paper.source_id in current_ids]


def _rank_papers(
    papers: list[Paper], config: AppConfig
) -> tuple[list[RankedPaper], list[str], int, int]:
    """Expand keywords, pre-sort, and LLM rank.

    Returns:
        Tuple of (ranked_papers, expanded_keywords, keyword_passed, keyword_rejected).
    """
    print("Expanding keywords...")
    expanded = expand_keywords(config.profile, config.llm)
    print(f"  Expanded to {len(expanded)} terms")

    # Pre-sort with expanded keywords
    expanded_profile = UserProfile(
        topic_interests=expanded,
        required_signals=config.profile.required_signals,
        negative_filters=config.profile.negative_filters,
    )

    keyword_passed = 0
    keyword_rejected = 0
    scored = []
    for p in papers:
        result = score_paper(p, expanded_profile)
        if result:
            scored.append((result.score, p))
            keyword_passed += 1
        else:
            keyword_rejected += 1

    scored.sort(key=lambda x: x[0], reverse=True)
    candidates = [p for _, p in scored[:50]]  # Cap at 50 for LLM
    print(f"  Pre-sort: {len(candidates)} candidates for LLM")

    if not candidates:
        return [], expanded, keyword_passed, keyword_rejected

    print("LLM ranking...")
    ranked = rerank_and_summarize(
        candidates,
        config.profile,
        config.llm,
        top_n=config.summary.max_papers,
    )
    return ranked, expanded, keyword_passed, keyword_rejected


def _generate_reports(
    ranked_papers: list[RankedPaper],
    config: AppConfig,
    total_fetched: int,
    expanded_keywords: list[str] | None = None,
    pipeline_stats: dict | None = None,
) -> tuple[str | None, str | None]:
    """Generate report files and return their paths."""
    output_dir = Path(config.output.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    md_path = None
    html_path = None

    if "markdown" in config.output.formats:
        md_name = timestamped_filename("digest", "md", model=config.llm.model)
        md_path = str(output_dir / md_name)
        md = generate_markdown_report(
            ranked_papers,
            token_usage=token_usage,
            profile=config.profile,
            sources_config=config.sources,
            total_fetched=total_fetched,
            model=config.llm.model,
            expanded_keywords=expanded_keywords or [],
            pipeline_stats=pipeline_stats or {},
        )
        with open(md_path, "w") as f:
            f.write(md)
        print(f"Markdown report: {md_path}")

    if "html" in config.output.formats:
        html_name = timestamped_filename("digest", "html", model=config.llm.model)
        html_path = str(output_dir / html_name)
        html = generate_html_report(
            ranked_papers,
            token_usage=token_usage,
            profile=config.profile,
            sources_config=config.sources,
            total_fetched=total_fetched,
            model=config.llm.model,
            expanded_keywords=expanded_keywords or [],
            pipeline_stats=pipeline_stats or {},
        )
        with open(html_path, "w") as f:
            f.write(html)
        print(f"HTML report: {html_path}")

    return md_path, html_path
