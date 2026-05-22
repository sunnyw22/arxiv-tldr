"""Mattermost incoming webhook integration for digest delivery.

Posts digest summaries via incoming webhook. The webhook URL is the only
secret needed — it encodes the target channel. Never log or expose it.
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone

import requests

from src.core.config import LLMConfig
from src.core.models import Paper
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.reports import SCORING_RUBRIC, short_model_name, source_label
from src.summarization.llm_client import call_llm

logger = logging.getLogger(__name__)

# Default per-message char budget. Mattermost servers cap post size (commonly
# 16383, sometimes 4000) and silently truncate anything over it, so we split
# rather than rely on the server. Override with MATTERMOST_MAX_POST_CHARS.
MAX_MESSAGE_LEN = 14000

# Section titles for the two summary buckets.
NEW_SECTION_TITLE = ":page_facing_up: Newly Published"
REPLACED_SECTION_TITLE = ":recycle: Re-published (v2+ updates)"


def _bot_name(model: str) -> str:
    """Generate a bot display name from the LLM model.

    Examples: 'T-GPT-5.4', 'T-Claude-sonnet-4'
    """
    name = short_model_name(model) if model else "LLM"
    return f"T-{name}"


def _generate_flavor(config: LLMConfig) -> tuple[str, str]:
    """Generate a funny quote and tagline via LLM.

    Returns (quote, tagline) tuple, or fallbacks if the call fails.
    """
    prompt = (
        "You are a daily research paper digest bot. "
        "You're an AI that reads all the arxiv papers so humans don't have to. "
        "Your tone is warmly sarcastic — like a friend who's genuinely trying to help "
        "but can't resist poking fun at the absurdity of academia, publish-or-perish culture, "
        "or the sheer volume of papers. Think: supportive colleague with dry wit, not evil AI overlord. "
        "Dark humor is welcome but it should feel affectionate, not threatening.\n"
        "Generate two things in exactly this format (no extra text):\n"
        "QUOTE: <a short funny quote, max 2 sentences, witty and self-aware>\n"
        "TAGLINE: <a one-sentence remark about presenting today's papers — "
        "e.g. something about saving the human from drowning in preprints, "
        "or a playful jab at their reading backlog>\n"
        "Do NOT use quotation marks. Be creative and different each time."
    )
    fallback_quote = "I read all the papers so you don't have to. You're welcome."
    fallback_tagline = (
        "Here are today's highlights — your reading backlog sends its regards."
    )
    try:
        light_config = LLMConfig(
            model=config.model,
            temperature=1.0,
            max_tokens=150,
        )
        raw = call_llm(prompt, light_config).strip()
        quote = fallback_quote
        tagline = fallback_tagline
        for line in raw.split("\n"):
            line = line.strip()
            if line.upper().startswith("QUOTE:"):
                quote = line.split(":", 1)[1].strip().strip('"')
            elif line.upper().startswith("TAGLINE:"):
                tagline = line.split(":", 1)[1].strip().strip('"')
        return quote, tagline
    except Exception:
        logger.warning("Flavor text generation failed, using fallbacks")
        return fallback_quote, fallback_tagline


def post_webhook(
    webhook_url: str,
    text: str,
    username: str = "Research Radar",
    icon_url: str = "",
) -> bool:
    """Send a message via Mattermost incoming webhook.

    Args:
        webhook_url: Full incoming webhook URL (secret — never log this).
        text: Message body (Mattermost markdown supported).
        username: Display name override for the bot post.
        icon_url: Optional avatar URL override.

    Returns:
        True on success, False on failure.
    """
    payload: dict = {
        "text": text,
        "username": username,
    }
    if icon_url:
        payload["icon_url"] = icon_url

    try:
        resp = requests.post(webhook_url, json=payload, timeout=30)
        resp.raise_for_status()
        logger.info("Webhook post succeeded")
        return True
    except Exception:
        # Log the error but NEVER log the webhook URL
        logger.exception("Failed to post via incoming webhook")
        return False


def _escape_pipe(text: str) -> str:
    """Escape pipe characters so they don't break Mattermost table columns."""
    return text.replace("|", "\\|")


def _field_tag(paper: Paper) -> str:
    """Return the field tag for a paper (e.g. 'cs.LG').

    Uses the arXiv primary category when present; falls back to a
    human-readable source label for non-arXiv papers.
    """
    cat = (paper.primary_category or "").strip()
    if cat:
        return cat
    return source_label(paper.source_type)


def _is_replacement(paper: Paper) -> bool:
    """True if the paper is a re-published / updated version (v2+).

    Primary signal: arXiv RSS 'arxiv_announce_type' — 'replace' and
    'replace-cross' indicate an updated version. 'new' and 'cross' are treated
    as newly published. Fallback (API mode, no announce_type): a version suffix
    greater than v1 in the source_id.
    """
    announce = str(paper.raw_metadata.get("arxiv_announce_type", "")).lower()
    if announce:
        return announce.startswith("replace")
    match = re.search(r"v(\d+)$", paper.source_id)
    if match:
        return int(match.group(1)) > 1
    return False


def format_intro_message(
    ranked_papers: list[RankedPaper],
    pipeline_stats: dict,
    model: str = "",
    llm_config: LLMConfig | None = None,
    profile: UserProfile | None = None,
) -> str:
    """Build the first message: intro + compact paper table.

    Args:
        ranked_papers: Scored papers (already filtered/sorted).
        pipeline_stats: Dict with pipeline statistics.
        model: LLM model name for attribution.
        llm_config: LLM config for quote generation.
        profile: User profile for context display.

    Returns:
        Markdown string for the intro message.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total_fetched = pipeline_stats.get("total_fetched", 0)
    bot = _bot_name(model)
    n_papers = len(ranked_papers)
    model_label = short_model_name(model) if model else ""

    # Generate flavor text (quote + tagline)
    quote = "I read all the papers so you don't have to. You're welcome."
    tagline = (
        "Here are today's highlights — your reading backlog sends its regards."
    )
    if llm_config:
        quote, tagline = _generate_flavor(llm_config)

    lines = [
        f"#### :robot: {bot} — Daily arXiv Scan — {today}",
        "",
        f"> *{quote}*",
        "",
        f"I have processed **{total_fetched} papers** announced on arXiv today. {tagline}",
        "",
    ]

    # Profile context
    if profile:
        lines.append("**Target profile:**")
        if profile.topic_interests:
            lines.append(f"- Topics: {', '.join(profile.topic_interests)}")
        if profile.project_context:
            lines.append(f"- Context: {profile.project_context.strip()}")
        if profile.expertise_level:
            lines.append(f"- Level: {profile.expertise_level}")
        lines.append("")

    lines.append("**Scoring rubric:**")
    lines.append(SCORING_RUBRIC)
    lines.append("")

    # Pipeline breakdown — show the real funnel: passed -> sent to LLM -> made the cut
    kw_passed = pipeline_stats.get("keyword_passed")
    kw_rejected = pipeline_stats.get("keyword_rejected")
    llm_candidates = pipeline_stats.get("llm_candidates")
    reused = pipeline_stats.get("reused_scored", 0)
    if kw_passed is not None:
        parts = [f"Keyword filter: {kw_passed} passed, {kw_rejected} rejected"]
        if llm_candidates:
            parts.append(f"{llm_candidates} sent to LLM")
        if reused:
            parts.append(f"{reused} reused from cache")
        parts.append(f"**{n_papers} made the cut**")
        lines.append(" · ".join(parts))
        lines.append("")

    # Compact paper table (score + field tag + title)
    if ranked_papers:
        lines.append("| Score | Field | Paper |")
        lines.append("|:---:|:---:|:---|")
        for rp in ranked_papers:
            link_url = rp.paper.source_url or rp.paper.pdf_url or ""
            title = _escape_pipe(rp.paper.title)
            title_cell = f"[{title}]({link_url})" if link_url else title
            tag = _escape_pipe(_field_tag(rp.paper))
            field_cell = f"`{tag}`" if tag else ""
            marker = " ♻️" if _is_replacement(rp.paper) else ""
            lines.append(
                f"| **{rp.relevance_score}** | {field_cell} | {title_cell}{marker} |"
            )
    else:
        lines.append(
            "No papers met the relevance threshold today. "
            "Either the field took a day off, or your standards are impressively high."
        )

    lines.append("")
    if model_label:
        lines.append(f"*Scored by {model_label}*")

    message = "\n".join(lines)
    if len(message) > MAX_MESSAGE_LEN:
        message = message[:MAX_MESSAGE_LEN] + "\n\n*... message truncated*"

    return message


def _paper_block(rp: RankedPaper) -> str:
    """Render one paper's detailed summary block (no trailing separator)."""
    title = _escape_pipe(rp.paper.title)
    link_url = rp.paper.source_url or rp.paper.pdf_url or ""
    tag = _escape_pipe(_field_tag(rp.paper))
    tag_str = f"`{tag}` " if tag else ""
    if link_url:
        header = f"{tag_str}**[{title}]({link_url})** (score: {rp.relevance_score})"
    else:
        header = f"{tag_str}**{title}** (score: {rp.relevance_score})"

    parts = [header]
    if rp.abstract_takeaway:
        parts.append(f"*{_escape_pipe(rp.abstract_takeaway)}*")
    if rp.why_relevant:
        parts.append(f"Why relevant: {_escape_pipe(rp.why_relevant)}")
    if rp.summary:
        parts.append(_escape_pipe(rp.summary))
    return "\n\n".join(parts)


def _pack_messages(header: str, blocks: list[str], max_chars: int) -> list[str]:
    """Pack paper blocks into one or more messages, each under max_chars.

    Splits only at paper boundaries so no paper is cut mid-block. A single
    paper larger than the budget is hard-truncated as a last resort. The
    section header is repeated with a '(cont.)' marker on continuation messages.
    """
    sep = "\n\n---\n\n"
    trunc_note = "\n\n*... summary truncated*"
    messages: list[str] = []
    chunk: list[str] = []
    chunk_len = len(header)

    def flush() -> None:
        nonlocal chunk, chunk_len
        if not chunk:
            return
        h = header if not messages else f"{header} (cont.)"
        messages.append(h + "\n\n" + sep.join(chunk))
        chunk = []
        chunk_len = len(header)

    for block in blocks:
        # A block too large to ever fit gets its own truncated message.
        if len(header) + len(sep) + len(block) > max_chars:
            flush()
            budget = max(max_chars - len(header) - len(sep) - len(trunc_note), 0)
            messages.append(header + "\n\n" + block[:budget] + trunc_note)
            continue
        added = len(block) + len(sep)
        if chunk and chunk_len + added > max_chars:
            flush()
        chunk.append(block)
        chunk_len += added

    flush()
    return messages


def format_summary_messages(
    ranked_papers: list[RankedPaper],
    section_title: str,
    max_chars: int = MAX_MESSAGE_LEN,
) -> list[str]:
    """Build one or more detailed-summary messages for a bucket of papers.

    Papers are rendered as per-paper blocks and packed into as many messages as
    needed to stay under max_chars, splitting only at paper boundaries so
    summaries are never silently truncated mid-paper. Mattermost auto-collapses
    long messages behind a "Show More" toggle, keeping the channel tidy.

    Args:
        ranked_papers: Scored papers for this bucket (already filtered/sorted).
        section_title: Section heading (e.g. "Newly Published").
        max_chars: Per-message character budget.

    Returns:
        List of markdown message strings (empty if no papers).
    """
    if not ranked_papers:
        return []
    header = f"#### {section_title} ({len(ranked_papers)})"
    blocks = [_paper_block(rp) for rp in ranked_papers]
    return _pack_messages(header, blocks, max_chars)


def send_digest_messages(
    webhook_url: str,
    ranked_papers: list[RankedPaper],
    pipeline_stats: dict,
    model: str = "",
    llm_config: LLMConfig | None = None,
    profile: UserProfile | None = None,
    max_chars: int | None = None,
) -> bool:
    """Send the digest to Mattermost as several messages.

    Message 1: Intro + profile + scoring rubric + compact paper table.
    Then detailed per-paper summaries, split into two buckets:
      - Newly published papers (arXiv 'new' / 'cross' announcements)
      - Re-published / v2+ updates (arXiv 'replace' announcements)
    Each bucket is further split into multiple messages when it exceeds the
    per-message budget, so summaries are never silently truncated. Empty
    buckets produce no message.

    Args:
        webhook_url: Incoming webhook URL (secret).
        ranked_papers: Scored papers.
        pipeline_stats: Pipeline statistics.
        model: LLM model name.
        llm_config: LLM config for quote generation.
        profile: User profile for context display.
        max_chars: Per-message char budget (defaults to MAX_MESSAGE_LEN).

    Returns:
        True if every message posted successfully.
    """
    budget = max_chars or MAX_MESSAGE_LEN
    bot = _bot_name(model)

    intro = format_intro_message(
        ranked_papers, pipeline_stats,
        model=model, llm_config=llm_config, profile=profile,
    )
    results = [post_webhook(webhook_url, intro, username=bot)]

    new_papers = [rp for rp in ranked_papers if not _is_replacement(rp.paper)]
    replaced_papers = [rp for rp in ranked_papers if _is_replacement(rp.paper)]

    for section_title, bucket in (
        (NEW_SECTION_TITLE, new_papers),
        (REPLACED_SECTION_TITLE, replaced_papers),
    ):
        for message in format_summary_messages(bucket, section_title, max_chars=budget):
            results.append(post_webhook(webhook_url, message, username=bot))

    return all(results)
