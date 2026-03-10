"""Tests for Mattermost incoming webhook integration."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import requests

from src.core.models import Paper
from src.ranking.rerank_llm import RankedPaper
from src.reports.mattermost import format_digest_message, post_webhook

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_paper(
    title="Test Paper", source_url="https://arxiv.org/abs/1234.5678"
):
    return Paper(
        source_id="1234.5678",
        title=title,
        authors=["Author One", "Author Two"],
        abstract="An abstract.",
        categories=["cs.LG"],
        primary_category="cs.LG",
        submitted_date=datetime(2026, 3, 9, tzinfo=timezone.utc),
        source_url=source_url,
        pdf_url="https://arxiv.org/pdf/1234.5678",
        source_type="arxiv_api",
    )


def _make_ranked(
    title="Test Paper",
    score=8,
    summary="A good paper.",
    source_url="https://arxiv.org/abs/1234.5678",
    abstract_takeaway="Key finding.",
):
    return RankedPaper(
        paper=_make_paper(title=title, source_url=source_url),
        relevance_score=score,
        reasoning="Relevant.",
        summary=summary,
        abstract_takeaway=abstract_takeaway,
    )


# ---------------------------------------------------------------------------
# TestFormatDigestMessage
# ---------------------------------------------------------------------------


class TestFormatDigestMessage:
    def test_basic_format(self):
        papers = [
            _make_ranked(title="Alpha Paper", score=9),
            _make_ranked(title="Beta Paper", score=7),
        ]
        stats = {"total_fetched": 50}
        msg = format_digest_message(papers, stats)

        assert "Research Radar" in msg
        assert "2 relevant" in msg
        assert "50 fetched" in msg
        assert "Alpha Paper" in msg
        assert "Beta Paper" in msg
        assert "**9**" in msg
        assert "**7**" in msg

    def test_empty_papers(self):
        msg = format_digest_message([], {"total_fetched": 50})

        assert "0 relevant" in msg
        assert "No papers met the relevance threshold" in msg

    def test_table_format(self):
        papers = [_make_ranked(score=8)]
        msg = format_digest_message(papers, {"total_fetched": 10})

        assert "| Score | Paper |" in msg
        assert "**8**" in msg

    def test_uses_abstract_takeaway(self):
        papers = [_make_ranked(abstract_takeaway="Important finding.")]
        msg = format_digest_message(papers, {"total_fetched": 10})

        assert "Important finding." in msg

    def test_falls_back_to_summary_first_sentence(self):
        papers = [
            _make_ranked(
                abstract_takeaway="",
                summary="First sentence. Second sentence.",
            )
        ]
        msg = format_digest_message(papers, {"total_fetched": 10})

        assert "First sentence." in msg
        assert "Second sentence" not in msg

    def test_paper_without_source_url_uses_pdf(self):
        papers = [_make_ranked(source_url="")]
        msg = format_digest_message(papers, {"total_fetched": 10})

        assert "[Test Paper](https://arxiv.org/pdf/1234.5678)" in msg

    def test_model_in_footer(self):
        papers = [_make_ranked()]
        msg = format_digest_message(
            papers, {"total_fetched": 10}, model="openai/gpt-4o-mini"
        )

        assert "Gpt-4o-mini" in msg

    def test_all_papers_count_in_footer(self):
        papers = [_make_ranked()]
        all_papers = [_make_paper()] * 100
        msg = format_digest_message(
            papers, {"total_fetched": 100}, all_papers=all_papers
        )

        assert "100 total papers scanned" in msg

    def test_pipeline_stats_shown(self):
        papers = [_make_ranked()]
        stats = {
            "total_fetched": 100,
            "keyword_passed": 20,
            "keyword_rejected": 80,
            "llm_scored": 20,
        }
        msg = format_digest_message(papers, stats)

        assert "20 passed" in msg
        assert "80 rejected" in msg

    def test_truncation_on_very_long_message(self):
        # Create many papers to exceed the limit
        papers = [
            _make_ranked(
                title=f"Paper with a very long title number {i} " * 5,
                abstract_takeaway="A " * 200,
            )
            for i in range(100)
        ]
        msg = format_digest_message(papers, {"total_fetched": 500})

        assert len(msg) <= 14100  # MAX_MESSAGE_LEN + truncation notice


# ---------------------------------------------------------------------------
# TestPostWebhook
# ---------------------------------------------------------------------------


class TestPostWebhook:
    @patch("src.reports.mattermost.requests.post")
    def test_successful_post(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_post.return_value = mock_resp

        result = post_webhook("https://mm.example.com/hooks/abc123", "hello")

        assert result is True
        mock_post.assert_called_once()
        body = mock_post.call_args.kwargs.get(
            "json", mock_post.call_args[1].get("json")
        )
        assert body["text"] == "hello"
        assert body["username"] == "Research Radar"

    @patch("src.reports.mattermost.requests.post")
    def test_custom_username(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_post.return_value = mock_resp

        post_webhook(
            "https://mm.example.com/hooks/abc123",
            "hello",
            username="Custom Bot",
        )

        body = mock_post.call_args.kwargs.get(
            "json", mock_post.call_args[1].get("json")
        )
        assert body["username"] == "Custom Bot"

    @patch("src.reports.mattermost.requests.post")
    def test_http_error_returns_false(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.side_effect = requests.HTTPError("403")
        mock_post.return_value = mock_resp

        result = post_webhook("https://mm.example.com/hooks/abc123", "hello")
        assert result is False

    @patch("src.reports.mattermost.requests.post")
    def test_connection_error_returns_false(self, mock_post):
        mock_post.side_effect = requests.ConnectionError("refused")

        result = post_webhook("https://mm.example.com/hooks/abc123", "hello")
        assert result is False

    @patch("src.reports.mattermost.requests.post")
    def test_icon_url_included_when_set(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_post.return_value = mock_resp

        post_webhook(
            "https://mm.example.com/hooks/abc123",
            "hello",
            icon_url="https://example.com/icon.png",
        )

        body = mock_post.call_args.kwargs.get(
            "json", mock_post.call_args[1].get("json")
        )
        assert body["icon_url"] == "https://example.com/icon.png"

    @patch("src.reports.mattermost.requests.post")
    def test_icon_url_omitted_when_empty(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_post.return_value = mock_resp

        post_webhook("https://mm.example.com/hooks/abc123", "hello")

        body = mock_post.call_args.kwargs.get(
            "json", mock_post.call_args[1].get("json")
        )
        assert "icon_url" not in body
