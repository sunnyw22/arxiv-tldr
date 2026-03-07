from datetime import datetime, timezone


def timestamped_filename(prefix: str = "digest", ext: str = "md", model: str = "") -> str:
    """Generate a timestamped report filename, e.g. digest_claude-sonnet_2026-03-07_1347.md"""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    # Extract short model name: "anthropic/claude-sonnet-4-20250514" -> "claude-sonnet-4"
    model_tag = ""
    if model:
        short = model.split("/")[-1]  # strip provider prefix
        # Remove date suffixes like -20250514
        parts = short.rsplit("-", 1)
        if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) >= 8:
            short = parts[0]
        model_tag = f"_{short}"
    return f"{prefix}{model_tag}_{ts}.{ext}"
