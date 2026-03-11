from datetime import datetime, timezone

from src.ranking.rerank_llm import RankedPaper


def short_model_name(model: str) -> str:
    """Extract short display name from litellm model string.

    E.g. "openai/gpt-4o-mini" -> "GPT-4o-mini"
         "anthropic/claude-sonnet-4-20250514" -> "Claude-sonnet-4"
    """
    if not model:
        return "LLM"
    short = model.split("/")[-1]  # strip provider prefix
    # Remove date suffixes like -20250514
    parts = short.rsplit("-", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) >= 8:
        short = parts[0]
    # Capitalize first letter for display
    return short[0].upper() + short[1:] if short else "LLM"


def timestamped_filename(prefix: str = "digest", ext: str = "md", model: str = "") -> str:
    """Generate a timestamped report filename, e.g. digest_gpt-4o_2026-03-07_1347.md"""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    model_tag = f"_{short_model_name(model).lower()}" if model else ""
    return f"{prefix}{model_tag}_{ts}.{ext}"


def source_label(source_type: str) -> str:
    """Return a human-readable source label for a paper."""
    if source_type in ("arxiv_api", "arxiv_rss", "arxiv"):
        return "arXiv"
    if source_type == "inspire":
        return "INSPIRE"
    return source_type


def get_date_range(ranked_papers: list[RankedPaper]) -> str:
    """Get the date range of papers in the results."""
    if not ranked_papers:
        return ""
    dates = [rp.paper.submitted_date for rp in ranked_papers]
    earliest = min(dates).strftime("%Y-%m-%d")
    latest = max(dates).strftime("%Y-%m-%d")
    if earliest == latest:
        return earliest
    return f"{earliest} to {latest}"


SCORING_RUBRIC = """| Score | Meaning |
|-------|---------|
| 9-10 | Directly addresses your active project or core methods. Must-read. |
| 7-8 | Same subfield with relevant methods or insights. Likely useful. |
| 4-6 | Adjacent field or tangentially related technique. Might be interesting. |
| 1-3 | Different field or minimal overlap with your work. |"""
