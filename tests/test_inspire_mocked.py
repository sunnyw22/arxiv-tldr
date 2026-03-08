"""Tests for INSPIRE API source with mocked HTTP calls."""

from unittest.mock import MagicMock, patch

import pytest

from src.sources.inspire import InspireAPI

# Realistic INSPIRE API response with different structure than arXiv
INSPIRE_RESPONSE = {
    "hits": {
        "total": 2,
        "hits": [
            {
                "id": "2845123",
                "metadata": {
                    "control_number": 2845123,
                    "titles": [{"title": "Track Reconstruction with Graph Neural Networks at ATLAS"}],
                    "abstracts": [
                        {"value": "We present a GNN-based approach to <b>track reconstruction</b>."},
                        {"value": "We present a GNN-based approach to track reconstruction in the ATLAS detector."},
                    ],
                    "authors": [
                        {"full_name": "Smith, John"},
                        {"full_name": "Zhang, Wei"},
                    ],
                    "collaborations": [],
                    "arxiv_eprints": [
                        {"value": "2603.01234", "categories": ["hep-ex", "cs.LG"]},
                    ],
                    "inspire_categories": [{"term": "Experiment-HEP"}],
                    "keywords": [
                        {"value": "tracking"},
                        {"value": "machine learning"},
                    ],
                    "earliest_date": "2026-03-07",
                    "dois": [{"value": "10.1234/example.2026"}],
                },
            },
            {
                "id": "2845999",
                "metadata": {
                    "control_number": 2845999,
                    "titles": [{"title": "Measurement of Higgs Boson Production"}],
                    "abstracts": [
                        {"value": "A measurement of Higgs boson production cross-sections."},
                    ],
                    "authors": [],
                    "collaborations": [{"value": "ATLAS"}],
                    "arxiv_eprints": [],
                    "inspire_categories": [{"term": "Experiment-HEP"}],
                    "keywords": [{"value": "Higgs"}],
                    "earliest_date": "2026",
                    "dois": [],
                },
            },
        ],
    }
}

INSPIRE_EMPTY_RESPONSE = {"hits": {"total": 0, "hits": []}}


class TestInspireAPI:
    @patch("src.sources.inspire.requests.get")
    def test_fetch_parses_papers(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["tracking"])
        assert len(papers) == 2

    @patch("src.sources.inspire.requests.get")
    def test_paper_with_arxiv_crossref(self, mock_get):
        """INSPIRE paper with arXiv eprint gets arXiv URLs and crossref in raw_metadata."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["tracking"])
        paper = papers[0]

        assert paper.source_id == "inspire:2845123"
        assert paper.source_type == "inspire"
        assert paper.raw_metadata["arxiv_id"] == "2603.01234"
        assert paper.source_url == "https://arxiv.org/abs/2603.01234"
        assert paper.pdf_url == "https://arxiv.org/pdf/2603.01234"
        assert "hep-ex" in paper.categories
        assert paper.raw_metadata["doi"] == "10.1234/example.2026"

    @patch("src.sources.inspire.requests.get")
    def test_collaboration_paper_no_individual_authors(self, mock_get):
        """Collaboration paper with no individual authors uses collaboration name."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["Higgs"])
        collab_paper = papers[1]

        assert collab_paper.authors == ["ATLAS Collaboration"]

    @patch("src.sources.inspire.requests.get")
    def test_paper_without_arxiv_uses_inspire_url(self, mock_get):
        """Paper without arXiv eprint uses INSPIRE URL and empty pdf_url."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["Higgs"])
        collab_paper = papers[1]

        assert "inspirehep.net/literature/2845999" in collab_paper.source_url
        assert collab_paper.pdf_url == ""

    @patch("src.sources.inspire.requests.get")
    def test_prefers_non_html_abstract(self, mock_get):
        """When multiple abstracts exist, prefers the one without HTML tags."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["tracking"])
        # First paper has HTML abstract first, plain second — should pick plain
        assert "<b>" not in papers[0].abstract
        assert "track reconstruction" in papers[0].abstract

    @patch("src.sources.inspire.requests.get")
    def test_date_parsing_full_date(self, mock_get):
        """YYYY-MM-DD date format parsed correctly."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["tracking"])
        assert papers[0].submitted_date.year == 2026
        assert papers[0].submitted_date.month == 3
        assert papers[0].submitted_date.day == 7

    @patch("src.sources.inspire.requests.get")
    def test_date_parsing_year_only(self, mock_get):
        """YYYY date format (no month/day) parsed as Jan 1."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["Higgs"])
        assert papers[1].submitted_date.year == 2026
        assert papers[1].submitted_date.month == 1

    @patch("src.sources.inspire.requests.get")
    def test_categories_merge_inspire_and_arxiv(self, mock_get):
        """Categories include both INSPIRE subject terms and arXiv categories."""
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["tracking"])
        cats = papers[0].categories
        assert "Experiment-HEP" in cats  # INSPIRE category
        assert "hep-ex" in cats  # arXiv category

    @patch("src.sources.inspire.requests.get")
    def test_empty_results(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = INSPIRE_EMPTY_RESPONSE
        mock_resp.raise_for_status = MagicMock()
        mock_get.return_value = mock_resp

        api = InspireAPI()
        papers = api.fetch(keywords=["nonexistent"])
        assert papers == []

    @patch("src.sources.inspire.requests.get")
    def test_network_error(self, mock_get):
        mock_get.side_effect = Exception("Connection refused")
        api = InspireAPI()
        with pytest.raises(Exception, match="Connection refused"):
            api.fetch(keywords=["tracking"])

    def test_build_query_keywords_and_subjects(self):
        api = InspireAPI()
        query = api._build_query(["tracking", "ML"], ["Experiment-HEP"], days_back=0)
        assert query == "find k tracking and k ML and subject Experiment-HEP"

    def test_build_query_keywords_only(self):
        api = InspireAPI()
        query = api._build_query(["tracking"], None, days_back=0)
        assert query == "find k tracking"

    def test_build_query_empty(self):
        api = InspireAPI()
        query = api._build_query(None, None)
        assert query == ""

    def test_build_query_includes_date_filter(self):
        api = InspireAPI()
        query = api._build_query(["tracking"], None, days_back=30)
        assert query.startswith("find k tracking and de >= ")
        # Verify date format YYYY-MM-DD
        import re
        assert re.search(r"de >= \d{4}-\d{2}-\d{2}$", query)

    def test_fetch_no_query_returns_empty(self):
        api = InspireAPI()
        papers = api.fetch(keywords=None, subject_codes=None)
        assert papers == []
