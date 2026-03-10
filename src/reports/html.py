from datetime import datetime, timezone

from src.core.config import SourcesConfig
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.reports import short_model_name
from src.reports.markdown import format_authors
from src.summarization.llm_client import TokenUsage


def _source_label(source_type: str) -> str:
    """Return a human-readable source label for a paper."""
    if source_type in ("arxiv_api", "arxiv_rss", "arxiv"):
        return "arXiv"
    if source_type == "inspire":
        return "INSPIRE"
    return source_type


def _source_badge_color(source_type: str) -> str:
    """Return a badge color for the source type."""
    if source_type in ("arxiv_api", "arxiv_rss", "arxiv"):
        return "#b31b1b"  # arXiv red
    if source_type == "inspire":
        return "#1a5276"  # INSPIRE blue
    return "#666"


def generate_html_report(
    ranked_papers: list[RankedPaper],
    token_usage: TokenUsage | None = None,
    profile: UserProfile | None = None,
    sources_config: SourcesConfig | None = None,
    total_fetched: int = 0,
    model: str = "",
    title: str = "Research Radar Digest",
    expanded_keywords: list[str] | None = None,
    pipeline_stats: dict | None = None,
) -> str:
    """Generate an HTML digest from ranked papers."""
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if expanded_keywords is None:
        expanded_keywords = []
    if pipeline_stats is None:
        pipeline_stats = {}

    # Date range from papers
    date_range = _get_date_range(ranked_papers)

    # Digest window
    digest_window = pipeline_stats.get("digest_window", "")
    digest_window_html = ""
    if digest_window:
        digest_window_html = f'<p class="digest-window">{_escape(digest_window)}</p>'

    # Search summary table
    summary_rows = ""
    if date_range:
        summary_rows += f"<tr><td>Paper date range</td><td>{_escape(date_range)}</td></tr>"
    summary_rows += f"<tr><td>Total papers fetched</td><td>{total_fetched}</td></tr>"
    summary_rows += f"<tr><td>Papers shown</td><td>{len(ranked_papers)}</td></tr>"
    if sources_config:
        if sources_config.arxiv.enabled and sources_config.arxiv.categories:
            cats = _escape(", ".join(sources_config.arxiv.categories))
            summary_rows += f"<tr><td>arXiv categories</td><td>{cats}</td></tr>"
        if sources_config.inspire.enabled:
            if sources_config.inspire.keywords:
                kws = _escape(", ".join(sources_config.inspire.keywords))
                summary_rows += f"<tr><td>INSPIRE keywords</td><td>{kws}</td></tr>"
            if sources_config.inspire.subject_codes:
                scs = _escape(", ".join(sources_config.inspire.subject_codes))
                summary_rows += f"<tr><td>INSPIRE subjects</td><td>{scs}</td></tr>"

    summary_html = f"""
    <div class="section">
        <h2>Search Summary</h2>
        <table class="summary-table">
            {summary_rows}
        </table>
    </div>
    """

    # User profile table
    profile_html = ""
    if profile:
        profile_rows = ""
        if profile.topic_interests:
            profile_rows += f"<tr><td>Topic interests</td><td>{_escape(', '.join(profile.topic_interests))}</td></tr>"
        if profile.required_signals:
            profile_rows += f"<tr><td>Required signals</td><td>{_escape(', '.join(profile.required_signals))}</td></tr>"
        if profile.negative_filters:
            profile_rows += f"<tr><td>Negative filters</td><td>{_escape(', '.join(profile.negative_filters))}</td></tr>"
        if profile.project_context:
            profile_rows += f"<tr><td>Project context</td><td>{_escape(profile.project_context)}</td></tr>"
        if profile.expertise_level:
            profile_rows += f"<tr><td>Expertise level</td><td>{_escape(profile.expertise_level)}</td></tr>"
        profile_html = f"""
        <div class="section">
            <h2>User Profile</h2>
            <table class="summary-table">
                {profile_rows}
            </table>
        </div>
        """

    # Synonym expansion section
    synonym_html = ""
    if expanded_keywords and profile and profile.topic_interests:
        original = _escape(", ".join(profile.topic_interests))
        expanded_str = _escape(", ".join(expanded_keywords))
        synonym_html = f"""
        <div class="section">
            <h2>Keyword Expansion</h2>
            <p><strong>Original interests:</strong> [{original}]</p>
            <p><strong>Expanded to:</strong> [{expanded_str}]</p>
        </div>
        """

    # Pipeline stats section
    stats_html = ""
    if pipeline_stats:
        stats_items = ""
        arxiv_count = pipeline_stats.get("arxiv_fetched", 0)
        inspire_count = pipeline_stats.get("inspire_fetched", 0)
        if arxiv_count or inspire_count:
            stats_items += f"<li><strong>Sources:</strong> {arxiv_count} from arXiv, {inspire_count} from INSPIRE</li>"
        unique = pipeline_stats.get("unique_papers")
        if unique is not None:
            stats_items += f"<li><strong>After dedup:</strong> {unique} unique papers</li>"
        kw_passed = pipeline_stats.get("keyword_passed")
        kw_rejected = pipeline_stats.get("keyword_rejected")
        if kw_passed is not None and kw_rejected is not None:
            stats_items += f"<li><strong>Keyword filter:</strong> {kw_passed} passed, {kw_rejected} rejected</li>"
        llm_scored = pipeline_stats.get("llm_scored")
        if llm_scored is not None:
            stats_items += f"<li><strong>LLM scored:</strong> {llm_scored} papers</li>"
        final_count = pipeline_stats.get("final_count")
        if final_count is not None:
            stats_items += f"<li><strong>Final digest:</strong> {final_count} papers</li>"
        if stats_items:
            stats_html = f"""
            <div class="section">
                <h2>Pipeline Stats</h2>
                <ul>{stats_items}</ul>
            </div>
            """

    # Scoring rubric
    rubric_html = """
    <div class="section">
        <h2>Scoring Rubric</h2>
        <table class="rubric">
            <tr><td class="score-cell" style="background-color: #2d8a4e; color: white;">9-10</td>
                <td>Directly addresses your active project or core methods. Must-read.</td></tr>
            <tr><td class="score-cell" style="background-color: #5a9e6f; color: white;">7-8</td>
                <td>Same subfield with relevant methods or insights. Likely useful.</td></tr>
            <tr><td class="score-cell" style="background-color: #b8860b; color: white;">4-6</td>
                <td>Adjacent field or tangentially related technique. Might be interesting.</td></tr>
            <tr><td class="score-cell" style="background-color: #999; color: white;">1-3</td>
                <td>Different field or minimal overlap with your work.</td></tr>
        </table>
    </div>
    """

    # Paper cards
    papers_html = ""
    for i, rp in enumerate(ranked_papers, 1):
        paper = rp.paper
        author_str = _escape(format_authors(paper.authors))
        pub_date = paper.submitted_date.strftime("%Y-%m-%d")
        score_color = _score_color(rp.relevance_score)
        source_tag = _source_label(paper.source_type)
        badge_color = _source_badge_color(paper.source_type)

        links = f'<a href="{paper.source_url}">Read paper</a>'
        if paper.pdf_url:
            links += f' | <a href="{paper.pdf_url}">PDF</a>'

        # Abstract dropdown
        abstract_html = ""
        if paper.abstract:
            abstract_html = f"""
            <details class="abstract">
                <summary>Abstract</summary>
                <p>{_escape(paper.abstract)}</p>
            </details>"""

        # Trust-structured sections
        model_label = short_model_name(model)
        trust_html = ""
        if rp.abstract_takeaway or rp.why_relevant:
            if rp.abstract_takeaway:
                trust_html += f"""
            <div class="trust-section from-paper">
                <span class="trust-label">From the paper:</span>
                <p>{_escape(rp.abstract_takeaway)}</p>
            </div>"""
            if rp.why_relevant:
                trust_html += f"""
            <div class="trust-section our-assessment">
                <span class="trust-label">{_escape(model_label)} - Assessment:</span>
                <p>{_escape(rp.why_relevant)}</p>
            </div>"""
        else:
            # Fallback for old entries without new fields
            trust_html = f"""
            <p class="reasoning"><strong>Why this matters:</strong> {_escape(rp.reasoning)}</p>
            <p class="summary"><strong>Summary:</strong> {_escape(rp.summary)}</p>"""

        papers_html += f"""
        <div class="paper">
            <h2>{i}. {_escape(paper.title)}</h2>
            <div class="meta">
                <span class="score" style="background-color: {score_color}">
                    {rp.relevance_score}/10
                </span>
                <span class="source-badge" style="background-color: {badge_color}">
                    {source_tag}
                </span>
                <span class="pub-date">Published: {pub_date}</span>
                <span class="categories">{_escape(', '.join(paper.categories[:5]))}</span>
            </div>
            <p class="authors">{author_str}</p>{abstract_html}{trust_html}
            <p class="links">{links}</p>
        </div>
        """

    footer_parts = []
    if model:
        footer_parts.append(f"Model: {_escape(model)}")
    if token_usage:
        footer_parts.append(_escape(token_usage.report()))
    footer = ""
    if footer_parts:
        footer = f'<p class="footer">{" | ".join(footer_parts)}</p>'

    no_papers = ""
    if not ranked_papers:
        no_papers = "<p>No papers matched your profile for this run.</p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_escape(title)}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #fafafa;
            color: #333;
        }}
        h1 {{
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        .subtitle {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        .digest-window {{
            background: #e8f4fd;
            border-left: 3px solid #0066cc;
            padding: 8px 14px;
            margin-bottom: 16px;
            font-size: 0.9em;
            color: #333;
        }}
        .paper {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        .paper h2 {{
            margin-top: 0;
            font-size: 1.1em;
        }}
        .meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }}
        .score {{
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .source-badge {{
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .pub-date {{
            color: #555;
            font-size: 0.85em;
        }}
        .categories {{
            color: #666;
            font-size: 0.85em;
        }}
        .authors {{
            color: #555;
            font-size: 0.9em;
            font-style: italic;
        }}
        .reasoning, .summary {{
            line-height: 1.6;
        }}
        .abstract {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 6px;
            padding: 10px 14px;
            margin: 10px 0;
            font-size: 0.9em;
        }}
        .abstract summary {{
            cursor: pointer;
            font-weight: bold;
            color: #555;
            font-size: 0.95em;
        }}
        .abstract p {{
            margin-top: 8px;
            line-height: 1.5;
            color: #444;
        }}
        .trust-section {{
            border-left: 3px solid #ddd;
            padding: 8px 14px;
            margin: 10px 0;
            border-radius: 0 6px 6px 0;
        }}
        .trust-section .trust-label {{
            font-weight: bold;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .trust-section p {{
            margin: 4px 0 0 0;
            line-height: 1.6;
        }}
        .from-paper {{
            background: #f0f7f0;
            border-left-color: #2d8a4e;
        }}
        .from-paper .trust-label {{
            color: #2d8a4e;
        }}
        .our-assessment {{
            background: #f0f4f8;
            border-left-color: #0066cc;
        }}
        .our-assessment .trust-label {{
            color: #0066cc;
        }}
        .links a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .links a:hover {{
            text-decoration: underline;
        }}
        .section {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 16px;
        }}
        .section h2 {{
            margin-top: 0;
            font-size: 1em;
            color: #555;
        }}
        .section ul {{
            margin: 0;
            padding-left: 20px;
        }}
        .section li {{
            margin-bottom: 4px;
            line-height: 1.5;
        }}
        .summary-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .summary-table td {{
            padding: 6px 12px;
            border-bottom: 1px solid #eee;
            font-size: 0.9em;
        }}
        .summary-table td:first-child {{
            font-weight: bold;
            width: 40%;
            color: #555;
        }}
        .rubric {{
            width: 100%;
            border-collapse: collapse;
        }}
        .rubric td {{
            padding: 6px 12px;
            border-bottom: 1px solid #eee;
            font-size: 0.9em;
        }}
        .score-cell {{
            width: 60px;
            text-align: center;
            font-weight: bold;
            border-radius: 4px;
        }}
        .footer {{
            color: #999;
            font-size: 0.8em;
            margin-top: 30px;
            text-align: center;
        }}
    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ],
            throwOnError: false
        }});"></script>
</head>
<body>
    <h1>{_escape(title)}</h1>
    <p class="subtitle">Generated: {now}</p>
    {digest_window_html}
    {summary_html}
    {profile_html}
    {synonym_html}
    {stats_html}
    {rubric_html}
    {no_papers}
    {papers_html}
    {footer}
</body>
</html>"""


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


def _score_color(score: int) -> str:
    """Return a color for the relevance score badge."""
    if score >= 8:
        return "#2d8a4e"
    if score >= 6:
        return "#5a9e6f"
    if score >= 4:
        return "#b8860b"
    return "#999"


def _escape(text: str) -> str:
    """Basic HTML escaping."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
