import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

import requests

from src.core.models import Paper
from src.sources.base import BaseSource

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"


class ArxivAPI(BaseSource):
    """Fetch papers from the arXiv API (Atom/OpenSearch)."""

    BASE_URL = "https://export.arxiv.org/api/query"

    def fetch(
        self,
        categories: list[str] | None = None,
        search_query: str | None = None,
        max_results: int = 50,
        start: int = 0,
    ) -> list[Paper]:
        """Fetch papers from the arXiv API.

        Args:
            categories: arXiv categories to filter by (OR'd together).
            search_query: Free-text search query (combined with categories via AND).
            max_results: Maximum number of results to return.
            start: Offset for pagination.
        """
        query = self._build_query(categories, search_query)
        if not query:
            return []

        params = {
            "search_query": query,
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=30)
        resp.raise_for_status()

        return self._parse_response(resp.text)

    def _build_query(self, categories: list[str] | None, search_query: str | None) -> str:
        """Build arXiv API query string.

        Uses space-separated operators (arXiv accepts both '+' and ' ' as delimiters,
        but requests URL-encodes '+' which breaks the query).
        """
        parts = []
        if categories:
            cat_query = " OR ".join(f"cat:{cat}" for cat in categories)
            if len(categories) > 1:
                cat_query = f"({cat_query})"
            parts.append(cat_query)
        if search_query:
            parts.append(f"all:{search_query}")
        return " AND ".join(parts)

    def _parse_response(self, xml_text: str) -> list[Paper]:
        """Parse arXiv API Atom XML response into Paper records."""
        root = ET.fromstring(xml_text)
        papers = []
        for entry in root.findall(f"{{{ATOM_NS}}}entry"):
            paper = self._parse_entry(entry)
            if paper:
                papers.append(paper)
        return papers

    def _parse_entry(self, entry: ET.Element) -> Paper | None:
        """Parse a single Atom entry into a Paper."""
        # ID: "http://arxiv.org/abs/2301.12345v1"
        id_text = entry.findtext(f"{{{ATOM_NS}}}id", "")
        arxiv_id = self._extract_arxiv_id(id_text)
        if not arxiv_id:
            return None

        title = entry.findtext(f"{{{ATOM_NS}}}title", "").strip()
        title = re.sub(r"\s+", " ", title)  # collapse whitespace

        abstract = entry.findtext(f"{{{ATOM_NS}}}summary", "").strip()
        abstract = re.sub(r"\s+", " ", abstract)

        authors = [
            name.text.strip()
            for author in entry.findall(f"{{{ATOM_NS}}}author")
            if (name := author.find(f"{{{ATOM_NS}}}name")) is not None and name.text
        ]

        categories = [
            cat.get("term", "")
            for cat in entry.findall(f"{{{ATOM_NS}}}category")
            if cat.get("term")
        ]

        primary_el = entry.find(f"{{{ARXIV_NS}}}primary_category")
        primary_category = primary_el.get("term", "") if primary_el is not None else (categories[0] if categories else "")

        published = entry.findtext(f"{{{ATOM_NS}}}published", "")
        updated = entry.findtext(f"{{{ATOM_NS}}}updated", "")

        submitted_date = self._parse_datetime(published)
        updated_date = self._parse_datetime(updated) if updated != published else None

        # Links
        source_url = f"https://arxiv.org/abs/{arxiv_id}"
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"

        # Comment
        comment = entry.findtext(f"{{{ARXIV_NS}}}comment", "")

        return Paper(
            source_id=arxiv_id,
            title=title,
            authors=authors,
            abstract=abstract,
            categories=categories,
            primary_category=primary_category,
            submitted_date=submitted_date,
            source_url=source_url,
            pdf_url=pdf_url,
            source_type="arxiv_api",
            updated_date=updated_date,
            raw_metadata={"comment": comment} if comment else {},
        )

    def _extract_arxiv_id(self, id_text: str) -> str | None:
        """Extract arXiv ID from Atom entry ID URL."""
        match = re.search(r"arxiv\.org/abs/([^\s?#]+)", id_text)
        return match.group(1) if match else None

    def _parse_datetime(self, dt_str: str) -> datetime:
        """Parse ISO datetime string from arXiv API."""
        if not dt_str:
            return datetime.now(timezone.utc)
        # Format: 2020-12-19T22:09:29Z
        dt_str = dt_str.replace("Z", "+00:00")
        return datetime.fromisoformat(dt_str)
