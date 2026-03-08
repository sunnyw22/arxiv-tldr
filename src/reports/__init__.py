from datetime import datetime, timezone


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
