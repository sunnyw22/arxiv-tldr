"""Tests for source modules with mocked network calls."""

from unittest.mock import MagicMock, patch

import pytest

from src.sources.arxiv_api import ArxivAPI

# Sample arXiv API XML response
ARXIV_API_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <title>ArXiv Query</title>
  <totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1</totalResults>
  <entry>
    <id>http://arxiv.org/abs/2603.01234v1</id>
    <title>Test Paper on Machine Learning</title>
    <summary>This paper studies machine learning methods for particle physics.</summary>
    <published>2026-03-07T12:00:00Z</published>
    <updated>2026-03-07T12:00:00Z</updated>
    <author><name>John Smith</name></author>
    <author><name>Jane Doe</name></author>
    <arxiv:primary_category term="hep-ex"/>
    <category term="hep-ex"/>
    <category term="cs.LG"/>
    <link href="http://arxiv.org/abs/2603.01234v1" rel="alternate" type="text/html"/>
    <link href="http://arxiv.org/pdf/2603.01234v1" title="pdf" rel="related" type="application/pdf"/>
  </entry>
</feed>"""

ARXIV_EMPTY_XML = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>ArXiv Query</title>
  <totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">0</totalResults>
</feed>"""


class TestArxivAPI:
    @patch("src.sources.arxiv_api.requests.get")
    def test_fetch_parses_papers(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = ARXIV_API_XML
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        api = ArxivAPI()
        papers = api.fetch(categories=["hep-ex"])
        assert len(papers) == 1
        assert papers[0].title == "Test Paper on Machine Learning"
        assert papers[0].source_id == "2603.01234v1"
        assert papers[0].source_type == "arxiv_api"
        assert "hep-ex" in papers[0].categories
        assert len(papers[0].authors) == 2

    @patch("src.sources.arxiv_api.requests.get")
    def test_fetch_empty_results(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = ARXIV_EMPTY_XML
        mock_response.status_code = 200
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        api = ArxivAPI()
        papers = api.fetch(categories=["hep-ex"])
        assert papers == []

    @patch("src.sources.arxiv_api.requests.get")
    def test_fetch_network_error(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        api = ArxivAPI()
        with pytest.raises(Exception, match="Network error"):
            api.fetch(categories=["hep-ex"])
