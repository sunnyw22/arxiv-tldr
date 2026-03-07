from datetime import datetime, timezone

from src.ranking.rerank_llm import RankedPaper
from src.summarization.llm_client import TokenUsage


def generate_html_report(
    ranked_papers: list[RankedPaper],
    token_usage: TokenUsage | None = None,
    title: str = "Research Radar Digest",
) -> str:
    """Generate an HTML digest from ranked papers.

    Args:
        ranked_papers: Papers with scores and summaries, sorted by relevance.
        token_usage: Optional token usage stats to include in footer.
        title: Report title.

    Returns:
        HTML string.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    papers_html = ""
    for i, rp in enumerate(ranked_papers, 1):
        paper = rp.paper
        author_str = ", ".join(paper.authors[:5])
        if len(paper.authors) > 5:
            author_str += f" et al. ({len(paper.authors)} authors)"

        score_color = _score_color(rp.relevance_score)

        links = f'<a href="{paper.source_url}">Read paper</a>'
        if paper.pdf_url:
            links += f' | <a href="{paper.pdf_url}">PDF</a>'

        papers_html += f"""
        <div class="paper">
            <h2>{i}. {_escape(paper.title)}</h2>
            <div class="meta">
                <span class="score" style="background-color: {score_color}">
                    {rp.relevance_score}/10
                </span>
                <span class="categories">{_escape(', '.join(paper.categories[:5]))}</span>
            </div>
            <p class="authors">{_escape(author_str)}</p>
            <p class="reasoning"><strong>Why this matters:</strong> {_escape(rp.reasoning)}</p>
            <p class="summary"><strong>Summary:</strong> {_escape(rp.summary)}</p>
            <p class="links">{links}</p>
        </div>
        """

    footer = ""
    if token_usage:
        footer = f'<p class="footer">{_escape(token_usage.report())}</p>'

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
        }}
        .score {{
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-weight: bold;
            font-size: 0.9em;
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
        .links a {{
            color: #0066cc;
            text-decoration: none;
        }}
        .links a:hover {{
            text-decoration: underline;
        }}
        .footer {{
            color: #999;
            font-size: 0.8em;
            margin-top: 30px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <h1>{_escape(title)}</h1>
    <p class="subtitle">Generated: {now} | Showing top {len(ranked_papers)} papers</p>
    {no_papers}
    {papers_html}
    {footer}
</body>
</html>"""


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
