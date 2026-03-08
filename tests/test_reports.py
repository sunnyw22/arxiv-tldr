"""Tests for report generation (markdown and HTML)."""


from src.core.config import ArxivSourceConfig, InspireSourceConfig, SourcesConfig
from src.reports import timestamped_filename
from src.reports.html import _escape, _score_color, generate_html_report
from src.reports.markdown import (
    _get_date_range,
    _normalize_name,
    format_authors,
    generate_markdown_report,
)


class TestFormatAuthors:
    def test_single_author(self):
        assert format_authors(["Smith, John"]) == "John Smith"

    def test_few_authors(self):
        result = format_authors(["Smith, John", "Doe, Jane"])
        assert result == "John Smith, Jane Doe"

    def test_more_than_five_authors(self):
        authors = [f"Author{i}, First{i}" for i in range(8)]
        result = format_authors(authors)
        assert "et al." in result
        assert "8 authors" in result

    def test_large_collaboration(self):
        # 100+ authors with ATLAS in the first few
        authors = ["ATLAS Collaboration"] + [f"Physicist{i}" for i in range(150)]
        result = format_authors(authors)
        assert "ATLAS Collaboration" in result
        assert "151 authors" in result

    def test_empty_authors(self):
        assert format_authors([]) == "Unknown"

    def test_no_comma_format(self):
        assert format_authors(["John Smith"]) == "John Smith"


class TestNormalizeName:
    def test_last_first(self):
        assert _normalize_name("Smith, John") == "John Smith"

    def test_already_normal(self):
        assert _normalize_name("John Smith") == "John Smith"


class TestGetDateRange:
    def test_single_date(self, sample_ranked_paper):
        result = _get_date_range([sample_ranked_paper])
        assert result == "2026-03-07"

    def test_date_range(self, sample_ranked_paper, sample_ranked_paper_2):
        result = _get_date_range([sample_ranked_paper, sample_ranked_paper_2])
        assert "2026-03-06" in result
        assert "2026-03-07" in result

    def test_empty(self):
        assert _get_date_range([]) == ""


class TestMarkdownReport:
    def test_basic_report(self, sample_ranked_paper, sample_profile):
        md = generate_markdown_report(
            [sample_ranked_paper],
            profile=sample_profile,
            total_fetched=30,
        )
        assert "Research Radar Digest" in md
        assert "Machine Learning for Particle Tracking" in md
        assert "8/10" in md
        assert "30" in md  # total fetched

    def test_empty_papers(self):
        md = generate_markdown_report([])
        assert "No papers matched" in md

    def test_includes_profile_section(self, sample_ranked_paper, sample_profile):
        md = generate_markdown_report([sample_ranked_paper], profile=sample_profile)
        assert "machine learning" in md
        assert "particle tracking" in md
        assert "advanced" in md

    def test_includes_sources(self, sample_ranked_paper):
        sources = SourcesConfig(
            arxiv=ArxivSourceConfig(enabled=True, categories=["hep-ex", "cs.LG"]),
            inspire=InspireSourceConfig(enabled=True, keywords=["tracking"]),
        )
        md = generate_markdown_report([sample_ranked_paper], sources_config=sources)
        assert "hep-ex" in md
        assert "tracking" in md

    def test_includes_scoring_rubric(self, sample_ranked_paper):
        md = generate_markdown_report([sample_ranked_paper])
        assert "Scoring Rubric" in md
        assert "9-10" in md

    def test_model_in_footer(self, sample_ranked_paper):
        md = generate_markdown_report([sample_ranked_paper], model="anthropic/claude-sonnet-4-20250514")
        assert "claude-sonnet" in md.lower() or "anthropic" in md.lower()

    def test_paper_links_preserved(self, sample_ranked_paper):
        md = generate_markdown_report([sample_ranked_paper])
        assert "arxiv.org/abs/2603.01234v1" in md
        assert "arxiv.org/pdf/2603.01234v1" in md


class TestHtmlReport:
    def test_basic_html(self, sample_ranked_paper, sample_profile):
        html = generate_html_report(
            [sample_ranked_paper],
            profile=sample_profile,
            total_fetched=30,
        )
        assert "<!DOCTYPE html>" in html
        assert "Machine Learning for Particle Tracking" in html
        assert "8/10" in html

    def test_empty_papers_html(self):
        html = generate_html_report([])
        assert "No papers matched" in html

    def test_score_colors(self):
        assert _score_color(9) == "#2d8a4e"
        assert _score_color(7) == "#5a9e6f"
        assert _score_color(5) == "#b8860b"
        assert _score_color(2) == "#999"

    def test_html_escaping(self):
        assert _escape("<script>alert('xss')</script>") == "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;" or \
               "&lt;script&gt;" in _escape("<script>alert('xss')</script>")


class TestTimestampedFilename:
    def test_basic_filename(self):
        name = timestamped_filename("digest", "md")
        assert name.startswith("digest_")
        assert name.endswith(".md")

    def test_model_in_filename(self):
        name = timestamped_filename("digest", "md", model="anthropic/claude-sonnet-4-20250514")
        assert "claude-sonnet-4" in name
        assert "20250514" not in name  # date suffix stripped

    def test_html_extension(self):
        name = timestamped_filename("digest", "html")
        assert name.endswith(".html")

    def test_no_model(self):
        name = timestamped_filename("digest", "md", model="")
        # Should not have double underscores from empty model
        assert "__" not in name
