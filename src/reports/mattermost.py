"""Mattermost incoming webhook integration for digest delivery.

Posts digest summaries via incoming webhook. The webhook URL is the only
secret needed — it encodes the target channel. Never log or expose it.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone

import requests

from src.ranking.rerank_llm import RankedPaper
from src.reports import short_model_name

logger = logging.getLogger(__name__)

# Mattermost message limit is 16383 chars; stay well under.
MAX_MESSAGE_LEN = 14000


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


def format_digest_message(
    ranked_papers: list[RankedPaper],
    pipeline_stats: dict,
    model: str = "",
    all_papers: list | None = None,
) -> str:
    """Build a compact Mattermost message for the daily digest.

    Keeps the message short to avoid spamming the channel:
    - Header with stats
    - Score table with paper titles and links
    - Truncates if too many papers

    Args:
        ranked_papers: Scored papers (already filtered/sorted).
        pipeline_stats: Dict with pipeline statistics.
        model: LLM model name for attribution.
        all_papers: All fetched papers (for total count display).

    Returns:
        Markdown string ready to post via webhook.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total_fetched = pipeline_stats.get("total_fetched", 0)
    n_papers = len(ranked_papers)
    model_label = short_model_name(model) if model else ""

    lines: list[str] = [
        f"#### :satellite: Research Radar — {today}",
        f"**{n_papers} relevant** from {total_fetched} fetched",
    ]

    # Pipeline breakdown (one line)
    kw_passed = pipeline_stats.get("keyword_passed")
    kw_rejected = pipeline_stats.get("keyword_rejected")
    if kw_passed is not None:
        lines.append(
            f"Keyword filter: {kw_passed} passed, {kw_rejected} rejected "
            f"| LLM scored: {pipeline_stats.get('llm_scored', '?')}"
        )
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
        lines.append("No papers met the relevance threshold today.")

    lines.append("")

    # Footer
    footer_parts = []
    if model_label:
        footer_parts.append(f"Model: {model_label}")
    if all_papers:
        footer_parts.append(f"{len(all_papers)} total papers scanned")
    if footer_parts:
        lines.append(f"*{' | '.join(footer_parts)}*")

    message = "\n".join(lines)

    # Truncate if too long
    if len(message) > MAX_MESSAGE_LEN:
        message = message[:MAX_MESSAGE_LEN] + "\n\n*... message truncated*"

    return message
