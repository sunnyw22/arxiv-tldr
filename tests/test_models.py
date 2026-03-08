"""Tests for core data models."""

from datetime import datetime, timezone

from src.core.models import Paper


class TestPaper:
    def test_paper_construction(self, sample_paper):
        assert sample_paper.source_id == "2603.01234v1"
        assert sample_paper.source_type == "arxiv_api"
        assert len(sample_paper.authors) == 3
        assert sample_paper.updated_date is None
        assert sample_paper.raw_metadata == {}

    def test_paper_with_all_fields(self):
        paper = Paper(
            source_id="test-123",
            title="Test",
            authors=["A"],
            abstract="Abstract",
            categories=["cs.AI"],
            primary_category="cs.AI",
            submitted_date=datetime(2026, 1, 1, tzinfo=timezone.utc),
            source_url="https://example.com",
            pdf_url="https://example.com/pdf",
            source_type="inspire",
            updated_date=datetime(2026, 2, 1, tzinfo=timezone.utc),
            raw_metadata={"key": "value"},
        )
        assert paper.updated_date is not None
        assert paper.raw_metadata["key"] == "value"
