"""Shared test fixtures for Research Radar tests."""

from datetime import datetime, timezone

import pytest

from src.core.config import (
    AppConfig,
    ArxivSourceConfig,
    InspireSourceConfig,
    LLMConfig,
    OutputConfig,
    SourcesConfig,
    SummaryConfig,
)
from src.core.models import Paper
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper


@pytest.fixture
def sample_profile():
    return UserProfile(
        topic_interests=["machine learning", "particle tracking"],
        required_signals=["ATLAS", "benchmark"],
        negative_filters=["survey only"],
        project_context="Applying ML to charged particle tracking in ATLAS.",
        expertise_level="advanced",
    )


@pytest.fixture
def sample_paper():
    return Paper(
        source_id="2603.01234v1",
        title="Machine Learning for Particle Tracking at the LHC",
        authors=["Smith, John", "Doe, Jane", "Zhang, Wei"],
        abstract=(
            "We present a novel machine learning approach to charged particle tracking in high-energy physics. "
            "Our method uses graph neural networks to reconstruct tracks in the ATLAS inner detector, achieving "
            "significant improvements in efficiency and purity compared to traditional methods."
        ),
        categories=["hep-ex", "cs.LG"],
        primary_category="hep-ex",
        submitted_date=datetime(2026, 3, 7, 12, 0, 0, tzinfo=timezone.utc),
        source_url="https://arxiv.org/abs/2603.01234v1",
        pdf_url="https://arxiv.org/pdf/2603.01234v1",
        source_type="arxiv_api",
    )


@pytest.fixture
def sample_paper_2():
    return Paper(
        source_id="2603.05678v1",
        title="Quantum Computing Applications in Cryptography",
        authors=["Alice, Bob"],
        abstract=(
            "We explore quantum computing applications for breaking RSA encryption. "
            "This paper focuses on post-quantum cryptographic protocols."
        ),
        categories=["quant-ph", "cs.CR"],
        primary_category="quant-ph",
        submitted_date=datetime(2026, 3, 6, 10, 0, 0, tzinfo=timezone.utc),
        source_url="https://arxiv.org/abs/2603.05678v1",
        pdf_url="https://arxiv.org/pdf/2603.05678v1",
        source_type="arxiv_api",
    )


@pytest.fixture
def sample_paper_negative():
    """A paper that should be rejected by negative filters."""
    return Paper(
        source_id="2603.09999v1",
        title="Survey Only: Overview of Recent ML Trends",
        authors=["Reviewer, Ann"],
        abstract="This is a survey only paper covering recent trends in machine learning.",
        categories=["cs.LG"],
        primary_category="cs.LG",
        submitted_date=datetime(2026, 3, 5, 8, 0, 0, tzinfo=timezone.utc),
        source_url="https://arxiv.org/abs/2603.09999v1",
        pdf_url="https://arxiv.org/pdf/2603.09999v1",
        source_type="arxiv_api",
    )


@pytest.fixture
def sample_ranked_paper(sample_paper):
    return RankedPaper(
        paper=sample_paper,
        relevance_score=8,
        reasoning="Directly addresses ML-based tracking in ATLAS, matching the researcher's core project.",
        summary="This paper presents a GNN-based approach to particle tracking in the ATLAS detector.",
    )


@pytest.fixture
def sample_ranked_paper_2(sample_paper_2):
    return RankedPaper(
        paper=sample_paper_2,
        relevance_score=3,
        reasoning="Quantum computing for cryptography has minimal overlap with particle physics ML.",
        summary="Explores quantum algorithms for RSA, unrelated to the researcher's HEP focus.",
    )


@pytest.fixture
def sample_config(sample_profile):
    return AppConfig(
        profile=sample_profile,
        sources=SourcesConfig(
            arxiv=ArxivSourceConfig(enabled=True, categories=["hep-ex", "cs.LG"]),
            inspire=InspireSourceConfig(enabled=True, keywords=["tracking"], subject_codes=["Experiment-HEP"]),
        ),
        summary=SummaryConfig(style="concise", max_papers=10),
        output=OutputConfig(formats=["markdown", "html"], output_dir="output/"),
        llm=LLMConfig(model="anthropic/claude-sonnet-4-20250514", temperature=0.3, max_tokens=4096),
    )


def make_paper(source_id="2603.00001v1", title="Test Paper", source_type="arxiv_api", **kwargs):
    """Helper to create Paper objects with sensible defaults."""
    defaults = dict(
        authors=["Author, Test"],
        abstract="Test abstract.",
        categories=["hep-ex"],
        primary_category="hep-ex",
        submitted_date=datetime(2026, 3, 7, 12, 0, 0, tzinfo=timezone.utc),
        source_url=f"https://arxiv.org/abs/{source_id}",
        pdf_url=f"https://arxiv.org/pdf/{source_id}",
        source_type=source_type,
    )
    defaults.update(kwargs)
    return Paper(source_id=source_id, title=title, **defaults)
