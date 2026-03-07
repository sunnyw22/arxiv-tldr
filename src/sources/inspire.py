import re
from datetime import datetime, timezone

import requests

from src.core.models import Paper
from src.sources.base import BaseSource

# Fields to request from INSPIRE API to keep responses lean
INSPIRE_FIELDS = (
    "titles,abstracts,authors.full_name,arxiv_eprints,"
    "keywords,inspire_categories,earliest_date,dois,control_number"
)


class InspireAPI(BaseSource):
    """Fetch papers from the INSPIRE-HEP API."""

    BASE_URL = "https://inspirehep.net/api/literature"

    def fetch(
        self,
        keywords: list[str] | None = None,
        subject_codes: list[str] | None = None,
        search_query: str | None = None,
        max_results: int = 50,
        page: int = 1,
    ) -> list[Paper]:
        """Fetch papers from INSPIRE-HEP.

        Args:
            keywords: INSPIRE keyword values (AND'd together).
                      e.g. ["tracking", "machine learning"]
            subject_codes: INSPIRE subject categories.
                           e.g. ["Experiment-HEP", "Computing"]
            search_query: Raw INSPIRE search query (SPIRES syntax).
                          Overrides keywords/subject_codes if provided.
            max_results: Number of results per page.
            page: Page number (1-indexed).
        """
        query = search_query or self._build_query(keywords, subject_codes)
        if not query:
            return []

        params = {
            "q": query,
            "sort": "mostrecent",
            "size": max_results,
            "page": page,
            "fields": INSPIRE_FIELDS,
        }

        resp = requests.get(self.BASE_URL, params=params, timeout=30)
        resp.raise_for_status()

        data = resp.json()
        papers = []
        for hit in data.get("hits", {}).get("hits", []):
            paper = self._parse_hit(hit)
            if paper:
                papers.append(paper)
        return papers

    def _build_query(
        self,
        keywords: list[str] | None,
        subject_codes: list[str] | None,
    ) -> str:
        """Build INSPIRE SPIRES-style search query.

        SPIRES syntax uses a single 'find' prefix with chained conditions:
          find k tracking and k machine learning and subject Experiment-HEP
        """
        conditions = []
        if keywords:
            for kw in keywords:
                conditions.append(f"k {kw}")
        if subject_codes:
            for sc in subject_codes:
                conditions.append(f"subject {sc}")
        if not conditions:
            return ""
        return "find " + " and ".join(conditions)

    def _parse_hit(self, hit: dict) -> Paper | None:
        """Parse a single INSPIRE API hit into a Paper."""
        meta = hit.get("metadata", {})
        inspire_id = str(meta.get("control_number", hit.get("id", "")))
        if not inspire_id:
            return None

        # Title — INSPIRE can have multiple titles from different sources
        titles = meta.get("titles", [])
        title = titles[0].get("title", "") if titles else ""
        if not title:
            return None

        # Authors
        authors = [
            a["full_name"]
            for a in meta.get("authors", [])
            if a.get("full_name")
        ]

        # Abstract — may have multiple from different sources, prefer non-HTML
        abstracts = meta.get("abstracts", [])
        abstract = self._pick_abstract(abstracts)

        # Categories — INSPIRE subject categories + arXiv categories if available
        inspire_cats = [c.get("term", "") for c in meta.get("inspire_categories", [])]
        arxiv_eprints = meta.get("arxiv_eprints", [])
        arxiv_cats = []
        arxiv_id = None
        if arxiv_eprints:
            arxiv_id = arxiv_eprints[0].get("value")
            arxiv_cats = arxiv_eprints[0].get("categories", [])

        categories = inspire_cats + arxiv_cats
        primary_category = inspire_cats[0] if inspire_cats else (arxiv_cats[0] if arxiv_cats else "")

        # Keywords
        keywords_list = [k.get("value", "") for k in meta.get("keywords", [])]

        # Date
        earliest_date = meta.get("earliest_date", "")
        submitted_date = self._parse_date(earliest_date)

        # URLs — prefer arXiv links if available, otherwise INSPIRE
        if arxiv_id:
            source_url = f"https://arxiv.org/abs/{arxiv_id}"
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        else:
            source_url = f"https://inspirehep.net/literature/{inspire_id}"
            pdf_url = ""

        # DOI
        dois = meta.get("dois", [])
        doi = dois[0].get("value", "") if dois else ""

        return Paper(
            source_id=f"inspire:{inspire_id}",
            title=title,
            authors=authors,
            abstract=abstract,
            categories=categories,
            primary_category=primary_category,
            submitted_date=submitted_date,
            source_url=source_url,
            pdf_url=pdf_url,
            source_type="inspire",
            raw_metadata={
                "inspire_id": inspire_id,
                "arxiv_id": arxiv_id,
                "keywords": keywords_list,
                "doi": doi,
            },
        )

    def _pick_abstract(self, abstracts: list[dict]) -> str:
        """Pick the best abstract — prefer non-HTML versions."""
        if not abstracts:
            return ""
        # Prefer abstracts without HTML tags
        for ab in abstracts:
            val = ab.get("value", "")
            if not re.search(r"<[^>]+>", val):
                return val.strip()
        # Fall back to first, strip HTML
        val = abstracts[0].get("value", "")
        return re.sub(r"<[^>]+>", "", val).strip()

    def _parse_date(self, date_str: str) -> datetime:
        """Parse INSPIRE date string (YYYY-MM-DD or YYYY)."""
        if not date_str:
            return datetime.now(timezone.utc)
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            try:
                return datetime.strptime(date_str, "%Y").replace(tzinfo=timezone.utc)
            except ValueError:
                return datetime.now(timezone.utc)
