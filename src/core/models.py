from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Paper:
    """Normalized paper record across all sources."""

    source_id: str
    title: str
    authors: list[str]
    abstract: str
    categories: list[str]
    primary_category: str
    submitted_date: datetime
    source_url: str
    pdf_url: str
    source_type: str  # "arxiv_rss", "arxiv_api", "inspire", etc.
    updated_date: datetime | None = None
    raw_metadata: dict[str, Any] = field(default_factory=dict)
