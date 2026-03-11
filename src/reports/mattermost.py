"""Mattermost incoming webhook integration for digest delivery.

Posts digest summaries via incoming webhook. The webhook URL is the only
secret needed — it encodes the target channel. Never log or expose it.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import requests

from src.core.config import LLMConfig
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.reports import SCORING_RUBRIC, short_model_name
from src.summarization.llm_client import call_llm

logger = logging.getLogger(__name__)

# Mattermost message limit is 16383 chars; stay well under.
MAX_MESSAGE_LEN = 14000


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


def format_intro_message(
    pipeline_stats: dict,
    model: str = "",
    llm_config: LLMConfig | None = None,
    profile: UserProfile | None = None,
) -> str:
    """Build the first message: funny intro + quote + profile + scoring rubric.

    Args:
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

    return "\n".join(lines)


def format_report_message(
    ranked_papers: list[RankedPaper],
    pipeline_stats: dict,
    model: str = "",
) -> str:
    """Build the second message: the actual scored paper table.

    Args:
        ranked_papers: Scored papers (already filtered/sorted).
        pipeline_stats: Dict with pipeline statistics.
        model: LLM model name for attribution.

    Returns:
        Markdown string for the report message.
    """
    n_papers = len(ranked_papers)
    model_label = short_model_name(model) if model else ""

    lines: list[str] = []

    # Pipeline breakdown
    kw_passed = pipeline_stats.get("keyword_passed")
    kw_rejected = pipeline_stats.get("keyword_rejected")
    llm_scored = pipeline_stats.get("llm_scored", 0)
    reused = pipeline_stats.get("reused_scored", 0)
    total_scored = llm_scored + reused
    if kw_passed is not None:
        parts = [f"Keyword filter: {kw_passed} passed, {kw_rejected} rejected"]
        parts.append(f"LLM scored: {total_scored}")
        parts.append(f"**{n_papers} made the cut**")
        lines.append(" | ".join(parts))
        lines.append("")

    if ranked_papers:
        lines.append("| Score | Paper |")
        lines.append("|:---:|:---|")
        for rp in ranked_papers:
            link_url = rp.paper.source_url or rp.paper.pdf_url or ""
            title = rp.paper.title
            if link_url:
                title_cell = f"[{title}]({link_url})"
            else:
                title_cell = title

            # Add one-line takeaway if available
            takeaway = rp.abstract_takeaway
            if not takeaway:
                takeaway = rp.summary.split(". ")[0] if rp.summary else ""
                if takeaway and not takeaway.endswith("."):
                    takeaway += "."
            if takeaway:
                title_cell += f" — *{takeaway}*"

            lines.append(f"| **{rp.relevance_score}** | {title_cell} |")
    else:
        lines.append(
            "No papers met the relevance threshold today. "
            "Either the field took a day off, or your standards are impressively high."
        )

    lines.append("")

    # Footer
    footer_parts = []
    if model_label:
        footer_parts.append(f"Scored by {model_label}")
    if footer_parts:
        lines.append(f"*{' | '.join(footer_parts)}*")

    message = "\n".join(lines)

    # Truncate if too long
    if len(message) > MAX_MESSAGE_LEN:
        message = message[:MAX_MESSAGE_LEN] + "\n\n*... message truncated*"

    return message


def send_digest_messages(
    webhook_url: str,
    ranked_papers: list[RankedPaper],
    pipeline_stats: dict,
    model: str = "",
    llm_config: LLMConfig | None = None,
    profile: UserProfile | None = None,
) -> bool:
    """Send the two-part digest to Mattermost.

    Message 1: Intro + quote of the day + profile + scoring rubric
    Message 2: Scored paper table

    Args:
        webhook_url: Incoming webhook URL (secret).
        ranked_papers: Scored papers.
        pipeline_stats: Pipeline statistics.
        model: LLM model name.
        llm_config: LLM config for quote generation.
        profile: User profile for context display.

    Returns:
        True if both messages posted successfully.
    """
    bot = _bot_name(model)

    intro = format_intro_message(
        pipeline_stats, model=model, llm_config=llm_config, profile=profile,
    )
    ok1 = post_webhook(webhook_url, intro, username=bot)

    report = format_report_message(ranked_papers, pipeline_stats, model=model)
    ok2 = post_webhook(webhook_url, report, username=bot)

    return ok1 and ok2
