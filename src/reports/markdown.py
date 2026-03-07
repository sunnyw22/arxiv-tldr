from datetime import datetime, timezone

from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.summarization.llm_client import TokenUsage

SCORING_RUBRIC = """| Score | Meaning |
|-------|---------|
| 9-10 | Directly addresses your active project or core methods. Must-read. |
| 7-8 | Same subfield with relevant methods or insights. Likely useful. |
| 4-6 | Adjacent field or tangentially related technique. Might be interesting. |
| 1-3 | Different field or minimal overlap with your work. |"""


def generate_markdown_report(
    ranked_papers: list[RankedPaper],
    token_usage: TokenUsage | None = None,
    profile: UserProfile | None = None,
    title: str = "Research Radar Digest",
) -> str:
    """Generate a markdown digest from ranked papers.

    Args:
        ranked_papers: Papers with scores and summaries, sorted by relevance.
        token_usage: Optional token usage stats to include in footer.
        profile: Optional user profile to display search context.
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

    # Search context
    if profile:
        lines.append("## Search Profile")
        lines.append("")
        if profile.topic_interests:
            lines.append(f"**Topic interests:** {', '.join(profile.topic_interests)}")
        if profile.project_context:
            lines.append(f"**Research context:** {profile.project_context}")
        if profile.expertise_level:
            lines.append(f"**Expertise level:** {profile.expertise_level}")
        lines.append("")

    # Scoring rubric
    lines.append("## Scoring Rubric")
    lines.append("")
    lines.append(SCORING_RUBRIC)
    lines.append("")

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
