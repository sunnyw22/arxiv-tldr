from dataclasses import dataclass, field
from datetime import datetime, timezone

from src.core.config import SourcesConfig
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.summarization.llm_client import TokenUsage

SCORING_RUBRIC = """| Score | Meaning |
|-------|---------|
| 9-10 | Directly addresses your active project or core methods. Must-read. |
| 7-8 | Same subfield with relevant methods or insights. Likely useful. |
| 4-6 | Adjacent field or tangentially related technique. Might be interesting. |
| 1-3 | Different field or minimal overlap with your work. |"""

# Large HEP collaborations — if all authors are from one of these, display as collaboration
KNOWN_COLLABORATIONS = {
    "ATLAS", "CMS", "LHCb", "ALICE", "Belle", "Belle II", "BaBar", "CDF",
    "D0", "DELPHI", "OPAL", "L3", "ALEPH", "STAR", "PHENIX", "BESIII",
    "T2K", "NOvA", "MicroBooNE", "DUNE", "IceCube", "Super-Kamiokande",
    "GRAPES-3", "Pierre Auger", "Fermi-LAT", "LIGO", "VIRGO",
}


def format_authors(authors: list[str]) -> str:
    """Format author list, detecting large collaborations."""
    if not authors:
        return "Unknown"

    # Check for collaboration papers (typically 100+ authors)
    if len(authors) > 50:
        # Look for collaboration name in first few authors or raw list
        for collab in KNOWN_COLLABORATIONS:
            for a in authors[:5]:
                if collab.lower() in a.lower():
                    return f"{collab} Collaboration ({len(authors)} authors)"
        return f"{authors[0]} et al. ({len(authors)} authors)"

    if len(authors) > 5:
        return ", ".join(authors[:5]) + f" *et al.* ({len(authors)} authors)"

    return ", ".join(authors)


def generate_markdown_report(
    ranked_papers: list[RankedPaper],
    token_usage: TokenUsage | None = None,
    profile: UserProfile | None = None,
    sources_config: SourcesConfig | None = None,
    total_fetched: int = 0,
    title: str = "Research Radar Digest",
) -> str:
    """Generate a markdown digest from ranked papers."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Date range from papers
    date_range = _get_date_range(ranked_papers)

    lines = [
        f"# {title}",
        f"*Generated: {now}*",
        "",
    ]

    # Search summary table
    lines.append("## Search Summary")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|-----------|-------|")
    if date_range:
        lines.append(f"| Paper date range | {date_range} |")
    lines.append(f"| Total papers fetched | {total_fetched} |")
    lines.append(f"| Papers shown | {len(ranked_papers)} |")
    if sources_config:
        if sources_config.arxiv.enabled and sources_config.arxiv.categories:
            lines.append(f"| arXiv categories | {', '.join(sources_config.arxiv.categories)} |")
        if sources_config.inspire.enabled:
            if sources_config.inspire.keywords:
                lines.append(f"| INSPIRE keywords | {', '.join(sources_config.inspire.keywords)} |")
            if sources_config.inspire.subject_codes:
                lines.append(f"| INSPIRE subjects | {', '.join(sources_config.inspire.subject_codes)} |")
    lines.append("")

    # Search profile
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
        pub_date = paper.submitted_date.strftime("%Y-%m-%d")

        lines.append(f"## {i}. {paper.title}")
        lines.append("")
        lines.append(f"**Relevance: {rp.relevance_score}/10** | "
                      f"Published: {pub_date} | "
                      f"Categories: {', '.join(paper.categories[:5])}")
        lines.append("")

        # Authors
        lines.append(f"**Authors:** {format_authors(paper.authors)}")
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


def _get_date_range(ranked_papers: list[RankedPaper]) -> str:
    """Get the date range of papers in the results."""
    if not ranked_papers:
        return ""
    dates = [rp.paper.submitted_date for rp in ranked_papers]
    earliest = min(dates).strftime("%Y-%m-%d")
    latest = max(dates).strftime("%Y-%m-%d")
    if earliest == latest:
        return earliest
    return f"{earliest} to {latest}"
