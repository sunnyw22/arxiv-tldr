"""Tests for the arXiv RSS source.

Covers parsing plus the failure modes that previously surfaced as a silent
"0 papers" result: transport errors, malformed feeds, and feeds arXiv has not
rebuilt for the current day yet.
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.sources.arxiv_rss import ArxivRSS


def _build_date_header(dt: datetime) -> str:
    return dt.strftime("%a, %d %b %Y %H:%M:%S +0000")


def _make_rss(entries: list[dict], build_date: datetime | None = None) -> str:
    """Generate an arXiv-style RSS 2.0 feed."""
    if build_date is None:
        build_date = datetime.now(timezone.utc)

    items = ""
    for e in entries:
        items += f"""
        <item>
            <title>{e['title']}</title>
            <link>https://arxiv.org/abs/{e['id']}</link>
            <description>{e.get('abstract', 'An abstract.')}</description>
            <dc:creator>{e.get('authors', 'Smith, John')}</dc:creator>
            <arxiv:announce_type>{e.get('announce_type', 'new')}</arxiv:announce_type>
            <category>{e.get('category', 'hep-ex')}</category>
        </item>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0"
         xmlns:dc="http://purl.org/dc/elements/1.1/"
         xmlns:arxiv="http://arxiv.org/schemas/atom">
        <channel>
            <title>hep-ex updates on arXiv.org</title>
            <lastBuildDate>{_build_date_header(build_date)}</lastBuildDate>
            {items}
        </channel>
    </rss>"""


def _resp(text: str) -> MagicMock:
    resp = MagicMock()
    resp.raise_for_status = MagicMock()
    resp.status_code = 200
    resp.text = text
    return resp


ONE_PAPER = [{"id": "2608.01001v1", "title": "Graph Networks for Track Finding"}]


class TestParsing:
    @patch("src.sources.arxiv_rss.requests.get")
    def test_parses_entries(self, mock_get):
        mock_get.return_value = _resp(_make_rss(ONE_PAPER))

        papers = ArxivRSS().fetch(categories=["hep-ex"])

        assert len(papers) == 1
        assert papers[0].source_id == "2608.01001v1"
        assert papers[0].title == "Graph Networks for Track Finding"
        assert papers[0].source_url == "https://arxiv.org/abs/2608.01001v1"
        assert papers[0].source_type == "arxiv_rss"

    @patch("src.sources.arxiv_rss.requests.get")
    def test_deduplicates_across_categories(self, mock_get):
        """The same paper cross-listed in two categories yields one Paper."""
        mock_get.return_value = _resp(_make_rss(ONE_PAPER))

        papers = ArxivRSS().fetch(categories=["hep-ex", "cs.LG"])

        assert len(papers) == 1
        assert mock_get.call_count == 2

    def test_no_categories_returns_empty(self):
        assert ArxivRSS().fetch(categories=[]) == []
        assert ArxivRSS().fetch(categories=None) == []

    @patch("src.sources.arxiv_rss.requests.get")
    def test_empty_but_fresh_feed_returns_empty(self, mock_get):
        """A quiet announcement day is not an error."""
        mock_get.return_value = _resp(_make_rss([], build_date=datetime.now(timezone.utc)))

        assert ArxivRSS().fetch(categories=["hep-ex"]) == []


class TestFailuresAreLoud:
    """Regression tests for the 2026-08-10 silent-empty-digest incident."""

    @patch("src.sources.arxiv_rss.requests.get")
    def test_http_error_raises(self, mock_get):
        resp = MagicMock()
        resp.raise_for_status.side_effect = requests.HTTPError("503 Server Error")
        mock_get.return_value = resp

        with pytest.raises(RuntimeError, match="all 1 arXiv RSS feeds failed"):
            ArxivRSS().fetch(categories=["hep-ex"])

    @patch("src.sources.arxiv_rss.requests.get", side_effect=requests.ConnectionError("no route to host"))
    def test_network_error_raises(self, mock_get):
        with pytest.raises(RuntimeError, match="no route to host"):
            ArxivRSS().fetch(categories=["hep-ex"])

    @patch("src.sources.arxiv_rss.requests.get")
    def test_malformed_feed_raises(self, mock_get):
        mock_get.return_value = _resp("this is not xml at all <<<>>>")

        with pytest.raises(RuntimeError, match="all 1 arXiv RSS feeds failed"):
            ArxivRSS().fetch(categories=["hep-ex"])

    @patch("src.sources.arxiv_rss.requests.get")
    def test_stale_feed_raises_with_rebuild_hint(self, mock_get):
        """Querying before arXiv's ~04:00 UTC rebuild must not look like a quiet day."""
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        mock_get.return_value = _resp(_make_rss([], build_date=yesterday))

        with pytest.raises(RuntimeError, match="not been rebuilt"):
            ArxivRSS().fetch(categories=["hep-ex"])

    @patch("src.sources.arxiv_rss.requests.get")
    def test_partial_failure_still_returns_papers(self, mock_get):
        """One dead category must not discard the categories that worked."""
        def side_effect(url, **kwargs):
            if "cs.LG" in url:
                raise requests.ConnectionError("cs.LG unreachable")
            return _resp(_make_rss(ONE_PAPER))

        mock_get.side_effect = side_effect

        papers = ArxivRSS().fetch(categories=["hep-ex", "cs.LG"])

        assert len(papers) == 1
