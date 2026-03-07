from datetime import datetime, timezone

from src.ranking.rerank_llm import RankedPaper
from src.summarization.llm_client import TokenUsage


def generate_markdown_report(
    ranked_papers: list[RankedPaper],
    token_usage: TokenUsage | None = None,
    title: str = "Research Radar Digest",
) -> str:
    """Generate a markdown digest from ranked papers.

    Args:
        ranked_papers: Papers with scores and summaries, sorted by relevance.
        token_usage: Optional token usage stats to include in footer.
        title: Report title.

    Returns:
        Markdown string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# {title}",
        f"*Generated: {now}*",
        f"*Papers reviewed: showing top {len(ranked_papers)}*",
        "",
    ]

    if not ranked_papers:
        lines.append("No papers matched your profile for this run.")
        return "\n".join(lines)

    lines.append("---")
    lines.append("")

    for i, rp in enumerate(ranked_papers, 1):
        paper = rp.paper
        lines.append(f"## {i}. {paper.title}")
        lines.append("")
        lines.append(f"**Relevance: {rp.relevance_score}/10** | "
                      f"Categories: {', '.join(paper.categories[:5])}")
        lines.append("")

        # Authors
        if paper.authors:
            author_str = ", ".join(paper.authors[:5])
            if len(paper.authors) > 5:
                author_str += f" *et al.* ({len(paper.authors)} authors)"
            lines.append(f"**Authors:** {author_str}")
            lines.append("")

        # Why relevant
        lines.append(f"**Why this matters:** {rp.reasoning}")
        lines.append("")

        # Summary
        lines.append(f"**Summary:** {rp.summary}")
        lines.append("")

        # Links
        lines.append(f"[Read paper]({paper.source_url})")
        if paper.pdf_url:
            lines.append(f" | [PDF]({paper.pdf_url})")
        lines.append("")
        lines.append("---")
        lines.append("")

    # Footer
    if token_usage:
        lines.append(f"*{token_usage.report()}*")
        lines.append("")

    return "\n".join(lines)
