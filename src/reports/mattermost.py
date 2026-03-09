"""Mattermost bot integration for digest delivery.

Posts summaries and uploads report files via the Mattermost REST API v4.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

import requests

from src.ranking.rerank_llm import RankedPaper

logger = logging.getLogger(__name__)


def _normalize_url(server_url: str) -> str:
    """Strip trailing slash from server URL."""
    return server_url.rstrip("/")


def upload_file(
    server_url: str, token: str, channel_id: str, file_path: str | Path
) -> str | None:
    """Upload a file to a Mattermost channel.

    POST multipart form data to /api/v4/files.

    Args:
        server_url: Mattermost server base URL (no trailing slash).
        token: Bot or personal access token.
        channel_id: Target channel ID.
        file_path: Local path to the file to upload.

    Returns:
        The file_id on success, None on failure.
    """
    url = f"{_normalize_url(server_url)}/api/v4/files"
    path = Path(file_path)

    try:
        with path.open("rb") as f:
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {token}"},
                data={"channel_id": channel_id},
                files={"files": (path.name, f)},
                timeout=60,
            )
        resp.raise_for_status()
        file_infos = resp.json().get("file_infos", [])
        if file_infos:
            file_id = file_infos[0]["id"]
            logger.info("Uploaded file %s (id=%s)", path.name, file_id)
            return file_id
        logger.warning("Upload response contained no file_infos")
        return None
    except Exception:
        logger.exception("Failed to upload file %s", file_path)
        return None


def create_post(
    server_url: str,
    token: str,
    channel_id: str,
    message: str,
    file_ids: list[str] | None = None,
) -> bool:
    """Create a post in a Mattermost channel.

    POST JSON to /api/v4/posts.

    Args:
        server_url: Mattermost server base URL (no trailing slash).
        token: Bot or personal access token.
        channel_id: Target channel ID.
        message: Post body (markdown supported).
        file_ids: Optional list of previously uploaded file IDs to attach.

    Returns:
        True on success, False on failure.
    """
    url = f"{_normalize_url(server_url)}/api/v4/posts"
    payload: dict = {
        "channel_id": channel_id,
        "message": message,
    }
    if file_ids:
        payload["file_ids"] = file_ids

    try:
        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        resp.raise_for_status()
        logger.info("Posted message to channel %s", channel_id)
        return True
    except Exception:
        logger.exception("Failed to create post in channel %s", channel_id)
        return False


def send_digest(
    server_url: str,
    token: str,
    channel_id: str,
    report_path: str | Path,
    summary: str,
) -> bool:
    """Send a digest to Mattermost: upload report file and post summary.

    Attempts to upload the report file first. If the upload succeeds, the
    summary is posted with the file attached. If the upload fails or the file
    doesn't exist, falls back to posting just the summary text.

    Args:
        server_url: Mattermost server base URL (no trailing slash).
        token: Bot or personal access token.
        channel_id: Target channel ID.
        report_path: Path to the generated report file.
        summary: Formatted summary text for the channel message.

    Returns:
        True if the post was sent (with or without attachment), False on
        total failure.
    """
    server_url = _normalize_url(server_url)

    # Only attempt upload if the file exists
    path = Path(report_path)
    file_id = None
    if path.exists():
        file_id = upload_file(server_url, token, channel_id, report_path)

    if file_id:
        return create_post(server_url, token, channel_id, summary, file_ids=[file_id])

    if not path.exists():
        logger.warning("Report file not found: %s; posting summary only", report_path)
    else:
        logger.warning("File upload failed; falling back to text-only post")
    return create_post(server_url, token, channel_id, summary)


def format_summary(
    ranked_papers: list[RankedPaper],
    pipeline_stats: dict,
) -> str:
    """Build a compact markdown summary for a Mattermost channel message.

    Args:
        ranked_papers: Scored and summarised papers (already filtered/sorted).
        pipeline_stats: Dict with at least ``total_fetched`` key.

    Returns:
        Markdown string ready to post.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total_fetched = pipeline_stats.get("total_fetched", 0)
    n_papers = len(ranked_papers)

    lines: list[str] = [
        f"### Research Radar Digest — {today}",
        f"**{n_papers} papers** scored from {total_fetched} fetched",
        "",
    ]

    if ranked_papers:
        lines.append("| Score | Paper |")
        lines.append("|-------|-------|")
        for rp in ranked_papers:
            link_url = rp.paper.source_url or rp.paper.pdf_url or ""
            if link_url:
                title_cell = f"[{rp.paper.title}]({link_url})"
            else:
                title_cell = rp.paper.title
            takeaway = rp.abstract_takeaway
            if not takeaway:
                takeaway = rp.summary.split(". ")[0]
                if takeaway and not takeaway.endswith("."):
                    takeaway += "."
            if takeaway:
                title_cell += f" — {takeaway}"
            lines.append(f"| {rp.relevance_score}/10 | {title_cell} |")
    else:
        lines.append("No papers met the relevance threshold today.")

    lines.append("")
    lines.append("*Generated by Research Radar*")

    return "\n".join(lines)
