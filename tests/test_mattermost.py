"""Tests for Mattermost incoming webhook integration."""

from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import requests

from src.core.config import LLMConfig
from src.core.models import Paper
from src.ranking.rerank_llm import RankedPaper
from src.reports.mattermost import (
    _bot_name,
    _escape_pipe,
    _field_tag,
    _is_replacement,
    format_intro_message,
    format_summary_messages,
    post_webhook,
    send_digest_messages,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_paper(
    title="Test Paper",
    source_url="https://arxiv.org/abs/1234.5678",
    source_id="1234.5678",
    primary_category="cs.LG",
    source_type="arxiv_rss",
    announce_type="new",
):
    raw_metadata = {"arxiv_announce_type": announce_type} if announce_type else {}
    return Paper(
        source_id=source_id,
        title=title,
        authors=["Author One", "Author Two"],
        abstract="An abstract.",
        categories=[primary_category] if primary_category else [],
        primary_category=primary_category,
        submitted_date=datetime(2026, 3, 9, tzinfo=timezone.utc),
        source_url=source_url,
        pdf_url="https://arxiv.org/pdf/1234.5678",
        source_type=source_type,
        raw_metadata=raw_metadata,
    )


def _make_ranked(
    title="Test Paper",
    score=8,
    summary="A good paper.",
    source_url="https://arxiv.org/abs/1234.5678",
    abstract_takeaway="Key finding.",
    why_relevant="Directly useful.",
    source_id="1234.5678",
    primary_category="cs.LG",
    announce_type="new",
):
    return RankedPaper(
        paper=_make_paper(
            title=title,
            source_url=source_url,
            source_id=source_id,
            primary_category=primary_category,
            announce_type=announce_type,
        ),
        relevance_score=score,
        reasoning="Relevant.",
        summary=summary,
        abstract_takeaway=abstract_takeaway,
        why_relevant=why_relevant,
    )


# ---------------------------------------------------------------------------
# TestEscapePipe
# ---------------------------------------------------------------------------


class TestEscapePipe:
    def test_escapes_pipe_in_math(self):
        assert _escape_pipe("P(A|B)") == "P(A\\|B)"

    def test_no_pipe_unchanged(self):
        assert _escape_pipe("hello world") == "hello world"

    def test_multiple_pipes(self):
        assert _escape_pipe("a|b|c") == "a\\|b\\|c"


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
        papers = [_make_ranked()]
        msg = format_intro_message(papers, stats, model="openai/gpt-5.4")

        assert "T-Gpt-5.4" in msg
        assert "500 papers" in msg
        assert "arXiv" in msg

    def test_contains_rubric(self):
        msg = format_intro_message([], {"total_fetched": 10})
        assert "9-10" in msg
        assert "Must-read" in msg
        assert "7-8" in msg

    def test_contains_quote(self):
        msg = format_intro_message([], {"total_fetched": 10})
        # Fallback quote when no llm_config
        assert "You're welcome" in msg

    def test_contains_paper_table(self):
        papers = [
            _make_ranked(title="Alpha Paper", score=9),
            _make_ranked(title="Beta Paper", score=7),
        ]
        stats = {"total_fetched": 50, "keyword_passed": 20, "keyword_rejected": 30, "llm_scored": 20}
        msg = format_intro_message(papers, stats)

        assert "| Score | Field | Paper |" in msg
        assert "Alpha Paper" in msg
        assert "Beta Paper" in msg
        assert "**9**" in msg
        assert "**7**" in msg
        assert "`cs.LG`" in msg
        assert "2 made the cut" in msg

    def test_empty_papers_shows_fallback(self):
        msg = format_intro_message([], {"total_fetched": 50})
        assert "impressively high" in msg

    def test_escapes_pipe_in_title(self):
        papers = [_make_ranked(title="P(A|B) Estimation")]
        msg = format_intro_message(papers, {"total_fetched": 10})
        assert "P(A\\|B)" in msg
        # Should not have an unescaped pipe breaking the table
        for line in msg.split("\n"):
            if "P(A" in line:
                # 3-column row | score | field | title | = 4 structural pipes,
                # plus 1 escaped pipe from the title's "\|" = 5 total.
                assert line.count("|") == 5

    @patch("src.reports.mattermost.call_llm")
    def test_generates_llm_flavor(self, mock_llm):
        mock_llm.return_value = (
            "QUOTE: Your papers are now my papers.\n"
            "TAGLINE: Resistance to reading is futile."
        )
        config = LLMConfig(model="openai/gpt-5.4")
        msg = format_intro_message(
            [], {"total_fetched": 10}, model="openai/gpt-5.4", llm_config=config
        )
        assert "Your papers are now my papers." in msg
        assert "Resistance to reading is futile." in msg
        mock_llm.assert_called_once()

    @patch("src.reports.mattermost.call_llm")
    def test_quote_fallback_on_error(self, mock_llm):
        mock_llm.side_effect = RuntimeError("API down")
        config = LLMConfig(model="openai/gpt-5.4")
        msg = format_intro_message(
            [], {"total_fetched": 10}, llm_config=config
        )
        assert "You're welcome" in msg

    def test_model_in_footer(self):
        papers = [_make_ranked()]
        msg = format_intro_message(papers, {"total_fetched": 10}, model="openai/gpt-5.4")
        assert "Gpt-5.4" in msg

    def test_truncation_on_very_long_message(self):
        papers = [
            _make_ranked(title=f"Paper with a very long title number {i} " * 5)
            for i in range(100)
        ]
        msg = format_intro_message(papers, {"total_fetched": 500})
        assert len(msg) <= 14100


# ---------------------------------------------------------------------------
# TestFormatSummaryMessage
# ---------------------------------------------------------------------------


class TestFormatSummaryMessages:
    def test_basic_format(self):
        papers = [
            _make_ranked(title="Alpha Paper", score=9),
            _make_ranked(title="Beta Paper", score=7),
        ]
        msgs = format_summary_messages(papers, "Newly Published")
        assert len(msgs) == 1
        msg = msgs[0]

        assert "Newly Published (2)" in msg
        assert "Alpha Paper" in msg
        assert "Beta Paper" in msg
        assert "score: 9" in msg
        assert "score: 7" in msg

    def test_empty_papers_returns_empty_list(self):
        assert format_summary_messages([], "Newly Published") == []

    def test_includes_takeaway(self):
        papers = [_make_ranked(abstract_takeaway="Important finding.")]
        msg = "\n".join(format_summary_messages(papers, "Newly Published"))
        assert "Important finding." in msg

    def test_includes_why_relevant(self):
        papers = [_make_ranked(why_relevant="Matches your research on X.")]
        msg = "\n".join(format_summary_messages(papers, "Newly Published"))
        assert "Matches your research on X." in msg

    def test_includes_summary(self):
        papers = [_make_ranked(summary="A detailed summary of the paper.")]
        msg = "\n".join(format_summary_messages(papers, "Newly Published"))
        assert "A detailed summary of the paper." in msg

    def test_includes_field_tag(self):
        papers = [_make_ranked(primary_category="hep-ex")]
        msg = "\n".join(format_summary_messages(papers, "Newly Published"))
        assert "`hep-ex`" in msg

    def test_escapes_pipe_in_content(self):
        papers = [_make_ranked(
            title="P(A|B) Methods",
            abstract_takeaway="Computes P(X|Y) efficiently.",
            summary="The method for P(A|B) is novel.",
        )]
        msg = "\n".join(format_summary_messages(papers, "Newly Published"))
        assert "P(A\\|B)" in msg
        assert "P(X\\|Y)" in msg

    def test_long_bucket_splits_without_losing_papers(self):
        # Each paper is large enough that 100 of them must span many messages.
        papers = [
            _make_ranked(
                title=f"Paper {i}",
                summary="A " * 500,
                abstract_takeaway="B " * 200,
            )
            for i in range(100)
        ]
        msgs = format_summary_messages(papers, "Newly Published", max_chars=14000)

        # Splits into multiple messages, each within budget.
        assert len(msgs) > 1
        for m in msgs:
            assert len(m) <= 14000
        # No paper is dropped and nothing is silently truncated.
        joined = "\n".join(msgs)
        for i in range(100):
            assert f"Paper {i}" in joined
        assert "truncated" not in joined
        # Continuation messages are marked.
        assert any("(cont.)" in m for m in msgs)

    def test_single_oversized_paper_is_truncated(self):
        papers = [_make_ranked(title="Huge", summary="X " * 20000)]
        msgs = format_summary_messages(papers, "Newly Published", max_chars=2000)
        assert len(msgs) == 1
        assert len(msgs[0]) <= 2000
        assert "truncated" in msgs[0]


# ---------------------------------------------------------------------------
# TestClassification (field tag + new vs v2)
# ---------------------------------------------------------------------------


class TestClassification:
    def test_field_tag_uses_primary_category(self):
        assert _field_tag(_make_paper(primary_category="cs.LG")) == "cs.LG"

    def test_field_tag_falls_back_to_source_label(self):
        paper = _make_paper(primary_category="", source_type="inspire")
        assert _field_tag(paper) == "INSPIRE"

    def test_new_announce_is_not_replacement(self):
        assert _is_replacement(_make_paper(announce_type="new")) is False

    def test_cross_announce_is_not_replacement(self):
        # Cross-listings are treated as newly published.
        assert _is_replacement(_make_paper(announce_type="cross")) is False

    def test_replace_announce_is_replacement(self):
        assert _is_replacement(_make_paper(announce_type="replace")) is True

    def test_replace_cross_announce_is_replacement(self):
        assert _is_replacement(_make_paper(announce_type="replace-cross")) is True

    def test_version_suffix_fallback_when_no_announce_type(self):
        # No announce_type (API mode): fall back to version suffix in source_id.
        v2 = _make_paper(source_id="2401.00001v2", announce_type=None)
        v1 = _make_paper(source_id="2401.00001v1", announce_type=None)
        assert _is_replacement(v2) is True
        assert _is_replacement(v1) is False


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
        mock_post.side_effect = [True, False]  # intro ok, summary fails

        result = send_digest_messages(
            "https://mm.example.com/hooks/abc",
            [_make_ranked()], {"total_fetched": 50},
        )

        assert result is False

    @patch("src.reports.mattermost.post_webhook")
    def test_skips_summary_when_no_papers(self, mock_post):
        mock_post.return_value = True

        result = send_digest_messages(
            "https://mm.example.com/hooks/abc",
            [], {"total_fetched": 50},
        )

        assert result is True
        # Only intro message posted, no summary
        assert mock_post.call_count == 1

    @patch("src.reports.mattermost.post_webhook")
    @patch("src.reports.mattermost._generate_flavor")
    def test_splits_new_and_v2_into_three_messages(self, mock_flavor, mock_post):
        mock_flavor.return_value = ("Quote.", "Tagline.")
        mock_post.return_value = True

        papers = [
            _make_ranked(title="Fresh A", announce_type="new"),
            _make_ranked(title="Fresh B", announce_type="cross"),
            _make_ranked(title="Updated C", announce_type="replace"),
        ]
        result = send_digest_messages(
            "https://mm.example.com/hooks/abc", papers, {"total_fetched": 50},
        )

        assert result is True
        # Intro + newly-published bucket + re-published bucket = 3 messages.
        assert mock_post.call_count == 3
        texts = [c.args[1] for c in mock_post.call_args_list]
        assert "Newly Published (2)" in texts[1]
        assert "Fresh A" in texts[1] and "Fresh B" in texts[1]
        assert "Re-published" in texts[2]
        assert "Updated C" in texts[2]

    @patch("src.reports.mattermost.post_webhook")
    @patch("src.reports.mattermost._generate_flavor")
    def test_only_v2_bucket_when_all_replacements(self, mock_flavor, mock_post):
        mock_flavor.return_value = ("Quote.", "Tagline.")
        mock_post.return_value = True

        papers = [_make_ranked(title="Updated", announce_type="replace")]
        send_digest_messages(
            "https://mm.example.com/hooks/abc", papers, {"total_fetched": 5},
        )

        # Intro + re-published bucket only (no empty new-papers message).
        assert mock_post.call_count == 2
        assert "Re-published" in mock_post.call_args_list[1].args[1]
