from datetime import datetime, timezone


def timestamped_filename(prefix: str = "digest", ext: str = "md") -> str:
    """Generate a timestamped report filename, e.g. digest_2026-03-07_1347.md"""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
    return f"{prefix}_{ts}.{ext}"
