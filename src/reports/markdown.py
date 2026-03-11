from datetime import datetime, timezone

from src.core.config import SourcesConfig
from src.core.models import Paper
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.reports import SCORING_RUBRIC, get_date_range, short_model_name, source_label
from src.summarization.llm_client import TokenUsage

# Large HEP collaborations — if all authors are from one of these, display as collaboration
KNOWN_COLLABORATIONS = {
    "ATLAS", "CMS", "LHCb", "ALICE", "Belle", "Belle II", "BaBar", "CDF",
    "D0", "DELPHI", "OPAL", "L3", "ALEPH", "STAR", "PHENIX", "BESIII",
    "T2K", "NOvA", "MicroBooNE", "DUNE", "IceCube", "Super-Kamiokande",
    "GRAPES-3", "Pierre Auger", "Fermi-LAT", "LIGO", "VIRGO",
}


def _normalize_name(name: str) -> str:
    """Convert 'Last, First' to 'First Last' for display."""
    if ", " in name:
        parts = name.split(", ", 1)
        return f"{parts[1]} {parts[0]}"
    return name


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
        return f"{_normalize_name(authors[0])} et al. ({len(authors)} authors)"

    display = [_normalize_name(a) for a in authors]

    if len(display) > 5:
        return ", ".join(display[:5]) + f" *et al.* ({len(authors)} authors)"

    return ", ".join(display)


def generate_markdown_report(
    ranked_papers: list[RankedPaper],
    token_usage: TokenUsage | None = None,
    profile: UserProfile | None = None,
    sources_config: SourcesConfig | None = None,
    total_fetched: int = 0,
    model: str = "",
    title: str = "Research Radar Digest",
    expanded_keywords: list[str] | None = None,
    pipeline_stats: dict | None = None,
    all_papers: list[Paper] | None = None,
) -> str:
    """Generate a markdown digest from ranked papers."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if expanded_keywords is None:
        expanded_keywords = []
    if pipeline_stats is None:
        pipeline_stats = {}

    # Date range from papers
    date_range = get_date_range(ranked_papers)

    lines = [
        f"# {title}",
        f"*Generated: {now}*",
        "",
    ]

    # Digest window
    digest_window = pipeline_stats.get("digest_window", "")
    if digest_window:
        lines.append(f"> {digest_window}")
        lines.append("")

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

    # User profile summary table
    if profile:
        lines.append("## User Profile")
        lines.append("")
        lines.append("| Field | Values |")
        lines.append("|-------|--------|")
        if profile.topic_interests:
            lines.append(f"| Topic interests | {', '.join(profile.topic_interests)} |")
        if profile.required_signals:
            lines.append(f"| Required signals | {', '.join(profile.required_signals)} |")
        if profile.negative_filters:
            lines.append(f"| Negative filters | {', '.join(profile.negative_filters)} |")
        if profile.project_context:
            lines.append(f"| Project context | {profile.project_context} |")
        if profile.expertise_level:
            lines.append(f"| Expertise level | {profile.expertise_level} |")
        lines.append("")

    # Synonym expansion table
    if expanded_keywords and profile and profile.topic_interests:
        lines.append("## Keyword Expansion")
        lines.append("")
        original = ", ".join(profile.topic_interests)
        expanded_str = ", ".join(expanded_keywords)
        lines.append(f"**Original interests:** [{original}]")
        lines.append(f"**Expanded to:** [{expanded_str}]")
        lines.append("")

    # Pipeline stats summary
    if pipeline_stats:
        lines.append("## Pipeline Stats")
        lines.append("")
        arxiv_count = pipeline_stats.get("arxiv_fetched", 0)
        inspire_count = pipeline_stats.get("inspire_fetched", 0)
        if arxiv_count or inspire_count:
            lines.append(f"- **Sources:** {arxiv_count} from arXiv, {inspire_count} from INSPIRE")
        unique = pipeline_stats.get("unique_papers")
        if unique is not None:
            lines.append(f"- **After dedup:** {unique} unique papers")
        kw_passed = pipeline_stats.get("keyword_passed")
        kw_rejected = pipeline_stats.get("keyword_rejected")
        if kw_passed is not None and kw_rejected is not None:
            lines.append(f"- **Keyword filter:** {kw_passed} passed, {kw_rejected} rejected")
        llm_scored = pipeline_stats.get("llm_scored")
        if llm_scored is not None:
            lines.append(f"- **LLM scored:** {llm_scored} papers")
        final_count = pipeline_stats.get("final_count")
        if final_count is not None:
            lines.append(f"- **Final digest:** {final_count} papers")
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
        source_tag = source_label(paper.source_type)

        lines.append(f"## {i}. {paper.title}")
        lines.append("")
        lines.append(f"**Relevance: {rp.relevance_score}/10** | "
                      f"Published: {pub_date} | "
                      f"Source: {source_tag} | "
                      f"Categories: {', '.join(paper.categories[:5])}")
        lines.append("")

        # Authors
        lines.append(f"**Authors:** {format_authors(paper.authors)}")
        lines.append("")

        # Abstract (collapsible)
        if paper.abstract:
            lines.append("<details>")
            lines.append("<summary>Abstract</summary>")
            lines.append("")
            lines.append(paper.abstract)
            lines.append("")
            lines.append("</details>")
            lines.append("")

        # Trust-structured sections
        model_label = short_model_name(model)
        if rp.abstract_takeaway:
            lines.append(f"**From the paper:** {rp.abstract_takeaway}")
            lines.append("")
        if rp.why_relevant:
            lines.append(f"**{model_label} - Assessment:** {rp.why_relevant}")
            lines.append("")

        # Fallback: show old-style summary/reasoning if new fields are empty
        if not rp.abstract_takeaway and not rp.why_relevant:
            lines.append(f"**Why this matters:** {rp.reasoning}")
            lines.append("")
            lines.append(f"**Summary:** {rp.summary}")
            lines.append("")

        # Links
        lines.append(f"[Read paper]({paper.source_url})")
        if paper.pdf_url:
            lines.append(f" | [PDF]({paper.pdf_url})")
        lines.append("")
        lines.append("---")
        lines.append("")

    # All fetched papers (collapsible, no LLM cost)
    if all_papers:
        ranked_ids = {rp.paper.source_id for rp in ranked_papers}
        other_papers = [p for p in all_papers if p.source_id not in ranked_ids]
        other_papers.sort(key=lambda p: p.submitted_date, reverse=True)
        lines.append("<details>")
        lines.append(f"<summary>All fetched papers ({len(all_papers)} total)</summary>")
        lines.append("")
        for p in all_papers:
            marker = " **[ranked]**" if p.source_id in ranked_ids else ""
            lines.append(f"- [{p.title}]({p.source_url}){marker}")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    # Footer
    footer_parts = []
    if model:
        footer_parts.append(f"Model: {model}")
    if token_usage:
        footer_parts.append(token_usage.report())
    if footer_parts:
        lines.append(f"*{' | '.join(footer_parts)}*")
        lines.append("")

    return "\n".join(lines)
