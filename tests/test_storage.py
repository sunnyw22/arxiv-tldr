"""Tests for SQLite storage layer."""


import pytest

from src.ranking.rerank_llm import RankedPaper
from src.storage.sqlite import (
    get_connection,
    get_known_source_ids,
    get_last_run_timestamp,
    get_run_papers,
    load_paper,
    paper_exists,
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
