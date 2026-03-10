"""Tests for Mattermost incoming webhook integration."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import requests

from src.core.config import LLMConfig
from src.core.models import Paper
from src.ranking.rerank_llm import RankedPaper
from src.reports.mattermost import (
    _bot_name,
    format_intro_message,
    format_report_message,
    post_webhook,
    send_digest_messages,
)

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
# TestBotName
# ---------------------------------------------------------------------------


class TestBotName:
    def test_gpt_model(self):
        assert _bot_name("openai/gpt-5.4") == "T-Gpt-5.4"

    def test_claude_model(self):
        assert _bot_name("anthropic/claude-sonnet-4-20250514") == "T-Claude-sonnet-4"

    def test_empty_model(self):
        assert _bot_name("") == "T-LLM"


# ---------------------------------------------------------------------------
# TestFormatIntroMessage
# ---------------------------------------------------------------------------


class TestFormatIntroMessage:
    def test_contains_date_and_count(self):
        stats = {"total_fetched": 500}
        msg = format_intro_message(stats, model="openai/gpt-5.4")

        assert "T-Gpt-5.4" in msg
        assert "500 papers" in msg
        assert "arXiv" in msg

    def test_contains_rubric(self):
        msg = format_intro_message({"total_fetched": 10})
        assert "9-10" in msg
        assert "Must-read" in msg
        assert "7-8" in msg

    def test_contains_quote(self):
        msg = format_intro_message({"total_fetched": 10})
        # Fallback quote when no llm_config
        assert "read all the papers" in msg

    @patch("src.reports.mattermost.call_llm")
    def test_generates_llm_flavor(self, mock_llm):
        mock_llm.return_value = (
            "QUOTE: Your papers are now my papers.\n"
            "TAGLINE: Resistance to reading is futile."
        )
        config = LLMConfig(model="openai/gpt-5.4")
        msg = format_intro_message(
            {"total_fetched": 10}, model="openai/gpt-5.4", llm_config=config
        )
        assert "Your papers are now my papers." in msg
        assert "Resistance to reading is futile." in msg
        mock_llm.assert_called_once()

    @patch("src.reports.mattermost.call_llm")
    def test_quote_fallback_on_error(self, mock_llm):
        mock_llm.side_effect = RuntimeError("API down")
        config = LLMConfig(model="openai/gpt-5.4")
        msg = format_intro_message(
            {"total_fetched": 10}, llm_config=config
        )
        assert "read all the papers" in msg


# ---------------------------------------------------------------------------
# TestFormatReportMessage
# ---------------------------------------------------------------------------


class TestFormatReportMessage:
    def test_basic_format(self):
        papers = [
            _make_ranked(title="Alpha Paper", score=9),
            _make_ranked(title="Beta Paper", score=7),
        ]
        stats = {"total_fetched": 50, "keyword_passed": 20, "keyword_rejected": 30, "llm_scored": 20}
        msg = format_report_message(papers, stats)

        assert "Alpha Paper" in msg
        assert "Beta Paper" in msg
        assert "**9**" in msg
        assert "**7**" in msg
        assert "2 made the cut" in msg

    def test_empty_papers(self):
        msg = format_report_message([], {"total_fetched": 50})
        assert "disappointing" in msg

    def test_table_format(self):
        papers = [_make_ranked(score=8)]
        msg = format_report_message(papers, {"total_fetched": 10})
        assert "| Score | Paper |" in msg
        assert "**8**" in msg

    def test_uses_abstract_takeaway(self):
        papers = [_make_ranked(abstract_takeaway="Important finding.")]
        msg = format_report_message(papers, {"total_fetched": 10})
        assert "Important finding." in msg

    def test_falls_back_to_summary_first_sentence(self):
        papers = [
            _make_ranked(abstract_takeaway="", summary="First sentence. Second sentence.")
        ]
        msg = format_report_message(papers, {"total_fetched": 10})
        assert "First sentence." in msg
        assert "Second sentence" not in msg

    def test_model_in_footer(self):
        papers = [_make_ranked()]
        msg = format_report_message(papers, {"total_fetched": 10}, model="openai/gpt-5.4")
        assert "Gpt-5.4" in msg

    def test_truncation_on_very_long_message(self):
        papers = [
            _make_ranked(
                title=f"Paper with a very long title number {i} " * 5,
                abstract_takeaway="A " * 200,
            )
            for i in range(100)
        ]
        msg = format_report_message(papers, {"total_fetched": 500})
        assert len(msg) <= 14100


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
        body = mock_post.call_args.kwargs.get("json", mock_post.call_args[1].get("json"))
        assert body["text"] == "hello"
        assert body["username"] == "Research Radar"

    @patch("src.reports.mattermost.requests.post")
    def test_custom_username(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.ok = True
        mock_post.return_value = mock_resp

        post_webhook("https://mm.example.com/hooks/abc123", "hello", username="T-Gpt-5.4")

        body = mock_post.call_args.kwargs.get("json", mock_post.call_args[1].get("json"))
        assert body["username"] == "T-Gpt-5.4"

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


# ---------------------------------------------------------------------------
# TestSendDigestMessages
# ---------------------------------------------------------------------------


class TestSendDigestMessages:
    @patch("src.reports.mattermost.post_webhook")
    @patch("src.reports.mattermost._generate_flavor")
    def test_sends_two_messages(self, mock_flavor, mock_post):
        mock_flavor.return_value = ("I'll be back... with papers.", "Your papers have been judged.")
        mock_post.return_value = True

        papers = [_make_ranked()]
        stats = {"total_fetched": 50}

        result = send_digest_messages(
            "https://mm.example.com/hooks/abc",
            papers, stats, model="openai/gpt-5.4",
        )

        assert result is True
        assert mock_post.call_count == 2

        # Both calls use the bot name
        for call in mock_post.call_args_list:
            assert call.kwargs.get("username", "") == "T-Gpt-5.4"

    @patch("src.reports.mattermost.post_webhook")
    @patch("src.reports.mattermost._generate_flavor")
    def test_returns_false_if_any_fails(self, mock_flavor, mock_post):
        mock_flavor.return_value = ("Quote.", "Tagline.")
        mock_post.side_effect = [True, False]  # intro ok, report fails

        result = send_digest_messages(
            "https://mm.example.com/hooks/abc",
            [_make_ranked()], {"total_fetched": 50},
        )

        assert result is False
