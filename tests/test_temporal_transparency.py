"""Tests for temporal semantics, report transparency, and configurable fetch parameters."""

import json
from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from src.core.config import AppConfig, LLMConfig, SummaryConfig, _parse_config
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.reports.html import generate_html_report
from src.reports.markdown import generate_markdown_report
from src.storage.sqlite import get_connection, get_source_checkpoint, save_source_checkpoint
from src.workflows.daily_digest import _filter_by_date, _rank_papers
from tests.conftest import make_paper

# --- max_results config parsing ---


class TestMaxResultsConfig:
    def test_default_max_results(self):
        config = _parse_config({})
        assert config.sources.arxiv.max_results == 50
        assert config.sources.inspire.max_results == 50

    def test_custom_max_results(self):
        raw = {
            "sources": {
                "arxiv": {"max_results": 100},
                "inspire": {"max_results": 25},
            }
        }
        config = _parse_config(raw)
        assert config.sources.arxiv.max_results == 100
        assert config.sources.inspire.max_results == 25

    def test_partial_max_results(self):
        raw = {"sources": {"arxiv": {"max_results": 75}}}
        config = _parse_config(raw)
        assert config.sources.arxiv.max_results == 75
        assert config.sources.inspire.max_results == 50  # default


# --- Date window filtering ---


class TestDateWindowFiltering:
    def test_filter_since(self):
        papers = [
            make_paper("p1", submitted_date=datetime(2026, 3, 5, tzinfo=timezone.utc)),
            make_paper("p2", submitted_date=datetime(2026, 3, 7, tzinfo=timezone.utc)),
            make_paper("p3", submitted_date=datetime(2026, 3, 9, tzinfo=timezone.utc)),
        ]
        since = datetime(2026, 3, 6, tzinfo=timezone.utc)
        result = _filter_by_date(papers, since_date=since, until_date=None)
        assert len(result) == 2
        assert all(p.submitted_date >= since for p in result)

    def test_filter_until(self):
        papers = [
            make_paper("p1", submitted_date=datetime(2026, 3, 5, tzinfo=timezone.utc)),
            make_paper("p2", submitted_date=datetime(2026, 3, 7, tzinfo=timezone.utc)),
            make_paper("p3", submitted_date=datetime(2026, 3, 9, tzinfo=timezone.utc)),
        ]
        until = datetime(2026, 3, 7, tzinfo=timezone.utc)
        result = _filter_by_date(papers, since_date=None, until_date=until)
        assert len(result) == 2
        assert all(p.submitted_date <= until for p in result)

    def test_filter_since_and_until(self):
        papers = [
            make_paper("p1", submitted_date=datetime(2026, 3, 5, tzinfo=timezone.utc)),
            make_paper("p2", submitted_date=datetime(2026, 3, 7, tzinfo=timezone.utc)),
            make_paper("p3", submitted_date=datetime(2026, 3, 9, tzinfo=timezone.utc)),
        ]
        since = datetime(2026, 3, 6, tzinfo=timezone.utc)
        until = datetime(2026, 3, 8, tzinfo=timezone.utc)
        result = _filter_by_date(papers, since_date=since, until_date=until)
        assert len(result) == 1
        assert result[0].source_id == "p2"

    def test_filter_no_dates(self):
        papers = [make_paper("p1"), make_paper("p2")]
        result = _filter_by_date(papers, since_date=None, until_date=None)
        assert len(result) == 2

    def test_filter_empty_result(self):
        papers = [
            make_paper("p1", submitted_date=datetime(2026, 3, 5, tzinfo=timezone.utc)),
        ]
        since = datetime(2026, 4, 1, tzinfo=timezone.utc)
        result = _filter_by_date(papers, since_date=since, until_date=None)
        assert len(result) == 0


# --- Source checkpoint save/load ---


class TestSourceCheckpoints:
    @pytest.fixture
    def db_conn(self, tmp_path):
        db_path = tmp_path / "test.db"
        conn = get_connection(db_path)
        yield conn
        conn.close()

    def test_save_and_get_checkpoint(self, db_conn):
        ts = datetime(2026, 3, 8, 12, 0, 0, tzinfo=timezone.utc)
        save_source_checkpoint(db_conn, "arxiv", ts, 42)
        result = get_source_checkpoint(db_conn, "arxiv")
        assert result is not None
        assert result.year == 2026
        assert result.month == 3
        assert result.day == 8

    def test_get_nonexistent_checkpoint(self, db_conn):
        result = get_source_checkpoint(db_conn, "nonexistent")
        assert result is None

    def test_update_checkpoint(self, db_conn):
        ts1 = datetime(2026, 3, 7, 12, 0, 0, tzinfo=timezone.utc)
        ts2 = datetime(2026, 3, 8, 12, 0, 0, tzinfo=timezone.utc)
        save_source_checkpoint(db_conn, "arxiv", ts1, 30)
        save_source_checkpoint(db_conn, "arxiv", ts2, 50)
        result = get_source_checkpoint(db_conn, "arxiv")
        assert result is not None
        assert result.day == 8

    def test_multiple_sources(self, db_conn):
        ts = datetime(2026, 3, 8, 12, 0, 0, tzinfo=timezone.utc)
        save_source_checkpoint(db_conn, "arxiv", ts, 30)
        save_source_checkpoint(db_conn, "inspire", ts, 20)
        assert get_source_checkpoint(db_conn, "arxiv") is not None
        assert get_source_checkpoint(db_conn, "inspire") is not None


# --- Report transparency sections ---


def _make_ranked_paper(source_type="arxiv_api"):
    paper = make_paper("2603.01234v1", "Test ML Paper", source_type=source_type)
    return RankedPaper(
        paper=paper,
        relevance_score=8,
        reasoning="Good match",
        summary="Summary text",
    )


def _make_inspire_ranked_paper():
    paper = make_paper(
        "inspire:12345", "INSPIRE Paper", source_type="inspire",
        source_url="https://inspirehep.net/literature/12345",
        pdf_url="",
    )
    return RankedPaper(
        paper=paper,
        relevance_score=6,
        reasoning="Some match",
        summary="Summary of inspire paper",
    )


class TestMarkdownTransparency:
    def test_profile_table(self):
        profile = UserProfile(
            topic_interests=["ML", "particle tracking"],
            required_signals=["ATLAS"],
            negative_filters=["survey only"],
            project_context="ML for tracking in ATLAS",
            expertise_level="advanced",
        )
        md = generate_markdown_report([_make_ranked_paper()], profile=profile)
        assert "## User Profile" in md
        assert "| Topic interests | ML, particle tracking |" in md
        assert "| Required signals | ATLAS |" in md
        assert "| Negative filters | survey only |" in md
        assert "| Project context | ML for tracking in ATLAS |" in md
        assert "| Expertise level | advanced |" in md

    def test_synonym_expansion(self):
        profile = UserProfile(topic_interests=["ML", "tracking"])
        expanded = ["ML", "machine learning", "deep learning", "tracking", "track reconstruction"]
        md = generate_markdown_report(
            [_make_ranked_paper()],
            profile=profile,
            expanded_keywords=expanded,
        )
        assert "## Keyword Expansion" in md
        assert "ML, tracking" in md
        assert "machine learning" in md
        assert "track reconstruction" in md

    def test_pipeline_stats(self):
        stats = {
            "arxiv_fetched": 30,
            "inspire_fetched": 20,
            "unique_papers": 45,
            "keyword_passed": 40,
            "keyword_rejected": 5,
            "llm_scored": 15,
            "final_count": 10,
            "digest_window": "Fetched 50 most recent papers",
        }
        md = generate_markdown_report(
            [_make_ranked_paper()],
            pipeline_stats=stats,
        )
        assert "## Pipeline Stats" in md
        assert "30 from arXiv" in md
        assert "20 from INSPIRE" in md
        assert "45 unique papers" in md
        assert "40 passed" in md
        assert "5 rejected" in md
        assert "15 papers" in md
        assert "10 papers" in md

    def test_digest_window(self):
        stats = {"digest_window": "Papers from 2026-03-01 to 2026-03-07"}
        md = generate_markdown_report([_make_ranked_paper()], pipeline_stats=stats)
        assert "Papers from 2026-03-01 to 2026-03-07" in md

    def test_source_tag_arxiv(self):
        md = generate_markdown_report([_make_ranked_paper()])
        assert "Source: arXiv" in md

    def test_source_tag_inspire(self):
        md = generate_markdown_report([_make_inspire_ranked_paper()])
        assert "Source: INSPIRE" in md

    def test_empty_expanded_keywords_no_section(self):
        md = generate_markdown_report([_make_ranked_paper()], expanded_keywords=[])
        assert "## Keyword Expansion" not in md

    def test_empty_pipeline_stats_no_section(self):
        md = generate_markdown_report([_make_ranked_paper()], pipeline_stats={})
        assert "## Pipeline Stats" not in md


class TestHtmlTransparency:
    def test_profile_table(self):
        profile = UserProfile(
            topic_interests=["ML", "particle tracking"],
            required_signals=["ATLAS"],
            negative_filters=["survey only"],
            project_context="ML for tracking in ATLAS",
            expertise_level="advanced",
        )
        html = generate_html_report([_make_ranked_paper()], profile=profile)
        assert "User Profile" in html
        assert "Topic interests" in html
        assert "Required signals" in html
        assert "Negative filters" in html
        assert "Project context" in html
        assert "Expertise level" in html

    def test_synonym_expansion(self):
        profile = UserProfile(topic_interests=["ML", "tracking"])
        expanded = ["ML", "machine learning", "deep learning"]
        html = generate_html_report(
            [_make_ranked_paper()],
            profile=profile,
            expanded_keywords=expanded,
        )
        assert "Keyword Expansion" in html
        assert "machine learning" in html

    def test_pipeline_stats(self):
        stats = {
            "arxiv_fetched": 30,
            "inspire_fetched": 20,
            "unique_papers": 45,
            "keyword_passed": 40,
            "keyword_rejected": 5,
            "llm_scored": 15,
            "final_count": 10,
        }
        html = generate_html_report([_make_ranked_paper()], pipeline_stats=stats)
        assert "Pipeline Stats" in html
        assert "30 from arXiv" in html
        assert "20 from INSPIRE" in html

    def test_digest_window(self):
        stats = {"digest_window": "Fetched 50 most recent papers"}
        html = generate_html_report([_make_ranked_paper()], pipeline_stats=stats)
        assert "Fetched 50 most recent papers" in html

    def test_source_badge(self):
        html = generate_html_report([_make_ranked_paper()])
        assert "source-badge" in html
        assert "arXiv" in html

    def test_inspire_source_badge(self):
        html = generate_html_report([_make_inspire_ranked_paper()])
        assert "source-badge" in html
        assert "INSPIRE" in html

    def test_no_synonym_section_when_empty(self):
        html = generate_html_report([_make_ranked_paper()], expanded_keywords=[])
        assert "Keyword Expansion" not in html


# --- Pipeline stats tracking (integration-level via _rank_papers) ---


class TestPipelineStatsTracking:
    """Test that _rank_papers returns keyword pass/reject counts."""

    def test_rank_papers_returns_keyword_counts(self):
        config = AppConfig(
            profile=UserProfile(
                topic_interests=["machine learning"],
                negative_filters=["survey only"],
            ),
            llm=LLMConfig(model="test/model"),
            summary=SummaryConfig(max_papers=5),
        )

        papers = [
            make_paper("p1", "ML for tracking", abstract="machine learning approach"),
            make_paper(
                "p2", "Survey Only: ML trends",
                abstract="This is a survey only paper",
            ),
            make_paper(
                "p3", "Deep learning methods",
                abstract="neural network approach to machine learning",
            ),
        ]

        mock_synonym_response = json.dumps({
            "expanded_terms": ["machine learning", "deep learning"]
        })
        mock_rank_response = json.dumps({
            "papers": [
                {
                    "paper_id": "p1",
                    "relevance_score": 8,
                    "reasoning": "Good",
                    "abstract_takeaway": "Key finding",
                    "why_relevant": "Relevant",
                    "summary": "Summary",
                },
                {
                    "paper_id": "p3",
                    "relevance_score": 7,
                    "reasoning": "Also good",
                    "abstract_takeaway": "Another finding",
                    "why_relevant": "Also relevant",
                    "summary": "Another summary",
                },
            ]
        })

        with (
            patch("src.ranking.synonym.call_llm", return_value=mock_synonym_response),
            patch("src.ranking.rerank_llm.call_llm", return_value=mock_rank_response),
        ):
            ranked, expanded, kw_passed, kw_rejected = _rank_papers(papers, config)

        assert kw_passed == 2  # p1 and p3 pass
        assert kw_rejected == 1  # p2 rejected by negative filter
        assert len(expanded) > 0
