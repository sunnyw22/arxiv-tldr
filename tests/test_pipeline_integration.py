"""Integration test for the full retrieval pipeline.

Mocks external calls (HTTP + LLM) but wires all internal modules together:
fetch → dedup → save to DB → score reuse check → LLM rank → report → save run.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.core.config import (
    AppConfig,
    ArxivSourceConfig,
    InspireSourceConfig,
    LLMConfig,
    OutputConfig,
    SourcesConfig,
    SummaryConfig,
)
from src.profiles.schema import UserProfile
from src.storage.sqlite import get_connection, load_paper
from src.workflows.daily_digest import run_daily_digest


def _make_arxiv_xml(papers: list[dict]) -> str:
    """Generate arXiv API XML response from paper dicts."""
    entries = ""
    for p in papers:
        cats = "".join(f'<category term="{c}"/>' for c in p.get("categories", ["hep-ex"]))
        authors = "".join(f"<author><name>{a}</name></author>" for a in p.get("authors", ["Test Author"]))
        primary = p.get("categories", ["hep-ex"])[0]
        entries += f"""
        <entry>
            <id>http://arxiv.org/abs/{p['id']}</id>
            <title>{p['title']}</title>
            <summary>{p['abstract']}</summary>
            <published>{p.get('date', '2026-03-07T12:00:00Z')}</published>
            <updated>{p.get('date', '2026-03-07T12:00:00Z')}</updated>
            {authors}
            <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="{primary}"/>
            {cats}
            <link href="http://arxiv.org/abs/{p['id']}" rel="alternate" type="text/html"/>
            <link href="http://arxiv.org/pdf/{p['id']}" title="pdf" rel="related" type="application/pdf"/>
        </entry>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom"
          xmlns:arxiv="http://arxiv.org/schemas/atom">
        <title>ArXiv Query</title>
        <totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">{len(papers)}</totalResults>
        {entries}
    </feed>"""


def _make_inspire_json(papers: list[dict]) -> dict:
    """Generate INSPIRE API JSON response from paper dicts."""
    hits = []
    for p in papers:
        hit = {
            "id": p["inspire_id"],
            "metadata": {
                "control_number": int(p["inspire_id"]),
                "titles": [{"title": p["title"]}],
                "abstracts": [{"value": p["abstract"]}],
                "authors": [{"full_name": a} for a in p.get("authors", ["Test Author"])],
                "collaborations": [],
                "arxiv_eprints": [],
                "inspire_categories": [{"term": "Experiment-HEP"}],
                "keywords": [],
                "earliest_date": p.get("date", "2026-03-07"),
                "dois": [],
            },
        }
        if "arxiv_id" in p:
            hit["metadata"]["arxiv_eprints"] = [
                {"value": p["arxiv_id"], "categories": p.get("categories", ["hep-ex"])}
            ]
        hits.append(hit)
    return {"hits": {"total": len(hits), "hits": hits}}


def _make_llm_ranking_response(paper_ids: list[str], scores: list[int] | None = None) -> str:
    """Generate mock LLM ranking JSON response."""
    if scores is None:
        scores = [8 - i for i in range(len(paper_ids))]
    return json.dumps({
        "papers": [
            {
                "paper_id": pid,
                "relevance_score": score,
                "reasoning": f"Relevant to researcher's interests (score {score})",
                "summary": f"Summary for paper {pid}",
            }
            for pid, score in zip(paper_ids, scores)
        ]
    })


def _make_llm_synonym_response() -> str:
    """Generate mock LLM synonym expansion response."""
    return json.dumps({
        "expanded_terms": [
            "machine learning", "deep learning", "neural networks",
            "particle tracking", "track reconstruction", "GNN",
        ]
    })


# -- Test paper data --

ARXIV_PAPERS = [
    {
        "id": "2603.01001v1",
        "title": "Graph Neural Networks for Track Finding",
        "abstract": "We apply GNNs to particle tracking in the ATLAS detector using machine learning.",
        "authors": ["Smith, John", "Doe, Jane"],
        "categories": ["hep-ex", "cs.LG"],
    },
    {
        "id": "2603.01002v1",
        "title": "Jet Tagging with Attention Networks",
        "abstract": "A new attention-based architecture for b-jet tagging at the LHC.",
        "authors": ["Zhang, Wei"],
        "categories": ["hep-ex"],
    },
    {
        "id": "2603.01003v1",
        "title": "Survey Only: Overview of HEP Computing",
        "abstract": "This is a survey only paper covering computing trends in HEP.",
        "authors": ["Reviewer, Ann"],
        "categories": ["hep-ex"],
    },
]

INSPIRE_PAPERS = [
    {
        "inspire_id": "2900001",
        "title": "Graph Neural Networks for Track Finding",
        "abstract": "We apply GNNs to particle tracking in the ATLAS detector.",
        "authors": ["Smith, John", "Doe, Jane"],
        "arxiv_id": "2603.01001",  # crossref → should dedup with arXiv paper
        "categories": ["hep-ex", "cs.LG"],
    },
    {
        "inspire_id": "2900002",
        "title": "New Trigger Algorithms for Run 4",
        "abstract": "Novel trigger algorithms for the high-luminosity LHC upgrade.",
        "authors": ["Trigger, Alice"],
    },
]

ARXIV_XML = _make_arxiv_xml(ARXIV_PAPERS)
INSPIRE_JSON = _make_inspire_json(INSPIRE_PAPERS)


@pytest.fixture
def pipeline_config(tmp_path):
    """Config for integration tests with output dir in tmp_path."""
    return AppConfig(
        profile=UserProfile(
            topic_interests=["machine learning", "particle tracking"],
            required_signals=["ATLAS"],
            negative_filters=["survey only"],
            project_context="ML for tracking in ATLAS",
            expertise_level="advanced",
        ),
        sources=SourcesConfig(
            arxiv=ArxivSourceConfig(enabled=True, categories=["hep-ex"]),
            inspire=InspireSourceConfig(enabled=True, keywords=["tracking"], subject_codes=["Experiment-HEP"]),
        ),
        summary=SummaryConfig(style="concise", max_papers=5),
        output=OutputConfig(formats=["markdown", "html"], output_dir=str(tmp_path / "output")),
        llm=LLMConfig(model="test/mock-model", temperature=0.3, max_tokens=4096),
    )


def _mock_requests_get_both(url, **kwargs):
    """Route mocked requests.get based on URL — arXiv vs INSPIRE."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.status_code = 200
    if "arxiv.org" in url:
        resp.text = ARXIV_XML
    elif "inspirehep.net" in url:
        resp.json.return_value = INSPIRE_JSON
    else:
        raise ValueError(f"Unexpected URL in mock: {url}")
    return resp


def _mock_requests_get_arxiv_only(url, **kwargs):
    """Mock that returns arXiv data and raises for INSPIRE."""
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.status_code = 200
    if "arxiv.org" in url:
        resp.text = ARXIV_XML
    elif "inspirehep.net" in url:
        raise Exception("INSPIRE is down")
    else:
        raise ValueError(f"Unexpected URL in mock: {url}")
    return resp


class TestFullPipeline:
    """Integration tests wiring the full pipeline with mocked externals."""

    @patch("src.sources.inspire.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.sources.arxiv_api.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.ranking.rerank_llm.call_llm")
    @patch("src.ranking.synonym.call_llm")
    def test_full_pipeline_produces_reports(
        self, mock_synonym_llm, mock_rank_llm, mock_arxiv_get, mock_inspire_get,
        pipeline_config, tmp_path,
    ):
        """Full pipeline: fetch from both sources → dedup → rank → generate reports."""
        mock_synonym_llm.return_value = _make_llm_synonym_response()
        mock_rank_llm.return_value = _make_llm_ranking_response(
            ["2603.01001v1", "2603.01002v1", "inspire:2900002"], [9, 7, 5],
        )

        db_path = tmp_path / "test.db"
        result = run_daily_digest(pipeline_config, db_path=db_path)

        # Pipeline should produce results
        assert result["ranked_papers"] is not None
        assert len(result["ranked_papers"]) > 0
        assert result["run_id"] is not None

        # Reports should be written
        assert result["md_path"] is not None
        assert result["html_path"] is not None
        assert Path(result["md_path"]).exists()
        assert Path(result["html_path"]).exists()

        # Markdown should contain paper titles
        md_content = Path(result["md_path"]).read_text()
        assert "Graph Neural Networks" in md_content

        # Stats should be populated
        stats = result["stats"]
        assert stats["total_fetched"] == 5  # 3 arXiv + 2 INSPIRE
        assert stats["unique_papers"] == 4  # one deduped

    @patch("src.sources.inspire.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.sources.arxiv_api.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.ranking.rerank_llm.call_llm")
    @patch("src.ranking.synonym.call_llm")
    def test_cross_source_dedup(
        self, mock_synonym_llm, mock_rank_llm, mock_arxiv_get, mock_inspire_get,
        pipeline_config, tmp_path,
    ):
        """INSPIRE paper with arXiv crossref should be deduplicated against arXiv paper."""
        mock_synonym_llm.return_value = _make_llm_synonym_response()
        mock_rank_llm.return_value = _make_llm_ranking_response(
            ["2603.01001v1", "2603.01002v1", "inspire:2900002"], [8, 6, 5],
        )

        db_path = tmp_path / "test.db"
        result = run_daily_digest(pipeline_config, db_path=db_path)

        stats = result["stats"]
        assert stats["total_fetched"] == 5  # 3 arXiv + 2 INSPIRE
        assert stats["unique_papers"] == 4  # one duplicate removed

    @patch("src.sources.inspire.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.sources.arxiv_api.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.ranking.rerank_llm.call_llm")
    @patch("src.ranking.synonym.call_llm")
    def test_negative_filter_excludes_paper(
        self, mock_synonym_llm, mock_rank_llm, mock_arxiv_get, mock_inspire_get,
        pipeline_config, tmp_path,
    ):
        """Paper matching negative_filter ('survey only') should not appear in results."""
        mock_synonym_llm.return_value = _make_llm_synonym_response()
        mock_rank_llm.return_value = _make_llm_ranking_response(
            ["2603.01001v1", "2603.01002v1", "inspire:2900002"], [8, 6, 5],
        )

        db_path = tmp_path / "test.db"
        result = run_daily_digest(pipeline_config, db_path=db_path)

        titles = [rp.paper.title for rp in result["ranked_papers"]]
        assert not any("Survey Only" in t for t in titles)

    @patch("src.sources.inspire.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.sources.arxiv_api.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.ranking.rerank_llm.call_llm")
    @patch("src.ranking.synonym.call_llm")
    def test_papers_persisted_to_db(
        self, mock_synonym_llm, mock_rank_llm, mock_arxiv_get, mock_inspire_get,
        pipeline_config, tmp_path,
    ):
        """All fetched papers (including filtered ones) should be saved to the DB."""
        mock_synonym_llm.return_value = _make_llm_synonym_response()
        mock_rank_llm.return_value = _make_llm_ranking_response(
            ["2603.01001v1", "2603.01002v1", "inspire:2900002"], [8, 6, 5],
        )

        db_path = tmp_path / "test.db"
        run_daily_digest(pipeline_config, db_path=db_path)

        # Verify papers are in DB (even the negative-filtered one)
        conn = get_connection(db_path)
        assert load_paper(conn, "2603.01001v1") is not None
        assert load_paper(conn, "2603.01002v1") is not None
        assert load_paper(conn, "2603.01003v1") is not None  # filtered but still saved
        assert load_paper(conn, "inspire:2900002") is not None  # INSPIRE paper
        conn.close()

    @patch("src.sources.inspire.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.sources.arxiv_api.requests.get", side_effect=_mock_requests_get_both)
    @patch("src.ranking.rerank_llm.call_llm")
    @patch("src.ranking.synonym.call_llm")
    def test_second_run_reuses_scores(
        self, mock_synonym_llm, mock_rank_llm, mock_arxiv_get, mock_inspire_get,
        pipeline_config, tmp_path,
    ):
        """Second run with same profile should reuse LLM scores from first run."""
        mock_synonym_llm.return_value = _make_llm_synonym_response()
        mock_rank_llm.return_value = _make_llm_ranking_response(
            ["2603.01001v1", "2603.01002v1", "inspire:2900002"], [8, 6, 5],
        )

        db_path = tmp_path / "test.db"

        # Run 1
        run_daily_digest(pipeline_config, db_path=db_path)
        rank_calls_after_run1 = mock_rank_llm.call_count

        # Run 2 — same config, same papers
        run_daily_digest(pipeline_config, db_path=db_path)
        rank_calls_after_run2 = mock_rank_llm.call_count

        # Second run should NOT call the ranking LLM (scores reused)
        assert rank_calls_after_run2 == rank_calls_after_run1

    @patch("src.sources.inspire.requests.get", side_effect=_mock_requests_get_arxiv_only)
    @patch("src.sources.arxiv_api.requests.get", side_effect=_mock_requests_get_arxiv_only)
    @patch("src.ranking.rerank_llm.call_llm")
    @patch("src.ranking.synonym.call_llm")
    def test_source_failure_doesnt_crash_pipeline(
        self, mock_synonym_llm, mock_rank_llm, mock_arxiv_get, mock_inspire_get,
        pipeline_config, tmp_path,
    ):
        """If one source fails, pipeline should still process papers from the other."""
        mock_synonym_llm.return_value = _make_llm_synonym_response()
        mock_rank_llm.return_value = _make_llm_ranking_response(
            ["2603.01001v1", "2603.01002v1"], [8, 6],
        )

        db_path = tmp_path / "test.db"
        result = run_daily_digest(pipeline_config, db_path=db_path)

        # Should still produce results from arXiv
        assert len(result["ranked_papers"]) > 0
        assert result["stats"]["total_fetched"] == 3  # only arXiv papers
