import re
from datetime import datetime, timezone

import feedparser

from src.core.models import Paper
from src.sources.base import BaseSource


class ArxivRSS(BaseSource):
    """Fetch papers from arXiv RSS/Atom feeds."""

    BASE_URL = "https://rss.arxiv.org/rss"

    def fetch(self, categories: list[str] | None = None) -> list[Paper]:
        """Fetch today's papers from arXiv RSS for given categories.

        Args:
            categories: arXiv categories to fetch (e.g. ["hep-ex", "cs.LG"]).
                         Fetches each category feed and deduplicates by arxiv ID.
        """
        if not categories:
            return []

        papers_by_id: dict[str, Paper] = {}
        for cat in categories:
            url = f"{self.BASE_URL}/{cat}"
            feed = feedparser.parse(url)
            for entry in feed.entries:
                paper = self._parse_entry(entry, cat)
                if paper and paper.source_id not in papers_by_id:
                    papers_by_id[paper.source_id] = paper
        return list(papers_by_id.values())

    def _parse_entry(self, entry: dict, feed_category: str) -> Paper | None:
        """Parse a single RSS feed entry into a Paper."""
        link = entry.get("link", "")
        arxiv_id = self._extract_arxiv_id(link)
        if not arxiv_id:
            return None

        # RSS title often has "(arXiv:XXXX.XXXXX ...)" suffix — clean it
        title = re.sub(r"\s*\(arXiv:[^)]+\)\s*$", "", entry.get("title", "")).strip()

        # Authors: dc:creator field, comma-separated or in <a> tags
        authors = self._parse_authors(entry)

        # Abstract: in description/summary, often wrapped in HTML <p> tags
        abstract = entry.get("summary", entry.get("description", ""))
        abstract = re.sub(r"<[^>]+>", "", abstract).strip()

        # Categories from tags if available, otherwise use feed category
        categories = [t.term for t in entry.get("tags", [])] if entry.get("tags") else [feed_category]

        # Primary category: first tag or feed category
        primary_category = categories[0] if categories else feed_category

        # Published date
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        submitted_date = datetime(*published[:6], tzinfo=timezone.utc) if published else datetime.now(timezone.utc)

        return Paper(
            source_id=arxiv_id,
            title=title,
            authors=authors,
            abstract=abstract,
            categories=categories,
            primary_category=primary_category,
            submitted_date=submitted_date,
            source_url=f"https://arxiv.org/abs/{arxiv_id}",
            pdf_url=f"https://arxiv.org/pdf/{arxiv_id}",
            source_type="arxiv_rss",
            raw_metadata=dict(entry),
        )

    def _extract_arxiv_id(self, link: str) -> str | None:
        """Extract arXiv ID from a URL like https://arxiv.org/abs/2301.12345"""
        match = re.search(r"arxiv\.org/abs/([^\s?#]+)", link)
        return match.group(1) if match else None

    def _parse_authors(self, entry: dict) -> list[str]:
        """Extract author names from RSS entry.

        arXiv RSS typically puts all authors in a single 'name' field,
        comma-separated. We split on commas to get individual names.
        """
        raw = ""
        if "authors" in entry:
            names = [a.get("name", "") for a in entry["authors"] if a.get("name")]
            raw = ", ".join(names)
        elif "author" in entry:
            raw = entry["author"]

        if not raw:
            return []

        # Strip HTML tags, then split on commas
        raw = re.sub(r"<[^>]+>", "", raw)
        return [a.strip() for a in raw.split(",") if a.strip()]
