"""Tests for report generation (markdown and HTML)."""


from src.core.config import ArxivSourceConfig, InspireSourceConfig, SourcesConfig
from src.ranking.rerank_llm import RankedPaper
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

    def test_abstract_in_collapsible(self, sample_ranked_paper):
        md = generate_markdown_report([sample_ranked_paper])
        assert "<details>" in md
        assert "<summary>Abstract</summary>" in md
        assert "graph neural networks" in md.lower()

    def test_trust_sections_with_new_fields(self, sample_paper):
        rp = RankedPaper(
            paper=sample_paper,
            relevance_score=8,
            reasoning="Good match",
            summary="Summary text",
            abstract_takeaway="Uses GNNs for tracking.",
            why_relevant="Directly applicable to your ATLAS project.",
        )
        md = generate_markdown_report([rp])
        assert "**From the paper:**" in md
        assert "Uses GNNs for tracking." in md
        assert "- Assessment:**" in md
        assert "Directly applicable to your ATLAS project." in md
        # Old-style fields should NOT appear when new fields are present
        assert "**Why this matters:**" not in md
        assert "**Summary:**" not in md

    def test_backwards_compat_old_fields(self, sample_ranked_paper):
        """When new fields are empty, fall back to old-style display."""
        md = generate_markdown_report([sample_ranked_paper])
        assert "**Why this matters:**" in md
        assert "**Summary:**" in md


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

    def test_abstract_in_html(self, sample_ranked_paper):
        html = generate_html_report([sample_ranked_paper])
        assert '<details class="abstract">' in html
        assert "<summary>Abstract</summary>" in html
        assert "graph neural networks" in html.lower()

    def test_trust_sections_html(self, sample_paper):
        rp = RankedPaper(
            paper=sample_paper,
            relevance_score=8,
            reasoning="Good match",
            summary="Summary text",
            abstract_takeaway="Uses GNNs for tracking.",
            why_relevant="Directly applicable to your ATLAS project.",
        )
        html = generate_html_report([rp])
        assert "from-paper" in html
        assert "our-assessment" in html
        assert "From the paper:" in html
        assert "- Assessment:" in html
        assert "Uses GNNs for tracking." in html

    def test_backwards_compat_html(self, sample_ranked_paper):
        """Old entries without new fields fall back to old-style display."""
        html = generate_html_report([sample_ranked_paper])
        assert "Why this matters:" in html
        assert "Summary:" in html

    def test_katex_cdn_links(self, sample_ranked_paper):
        """HTML report includes KaTeX CDN resources for LaTeX rendering."""
        html = generate_html_report([sample_ranked_paper])
        assert "katex.min.css" in html
        assert "katex.min.js" in html
        assert "auto-render.min.js" in html

    def test_katex_auto_render_script(self):
        """HTML report includes auto-render initialization with correct config."""
        html = generate_html_report([])
        assert "renderMathInElement" in html
        assert "throwOnError: false" in html
        assert "display: true" in html
        assert "display: false" in html


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
