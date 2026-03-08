"""Tests for keyword-based paper scoring."""

from src.profiles.schema import UserProfile
from src.ranking.keyword import score_paper


class TestScorePaper:
    def test_matching_interests_score(self, sample_paper, sample_profile):
        result = score_paper(sample_paper, sample_profile)
        assert result is not None
        assert result.score >= 2.0  # "machine learning" + "particle tracking"
        assert "machine learning" in result.matched_interests

    def test_required_signals_bonus(self, sample_paper, sample_profile):
        result = score_paper(sample_paper, sample_profile)
        assert result is not None
        assert "ATLAS" in result.matched_signals
        assert result.score >= 2.5  # interests + signal bonus

    def test_negative_filter_rejects(self, sample_paper_negative, sample_profile):
        result = score_paper(sample_paper_negative, sample_profile)
        assert result is None

    def test_no_match_rejected(self, sample_paper_2, sample_profile):
        result = score_paper(sample_paper_2, sample_profile)
        assert result is None

    def test_case_insensitive_matching(self, sample_profile):
        from tests.conftest import make_paper

        paper = make_paper(title="MACHINE LEARNING for Physics", abstract="Using ML and ATLAS data")
        result = score_paper(paper, sample_profile)
        assert result is not None
        assert "machine learning" in result.matched_interests

    def test_empty_profile_rejected(self, sample_paper):
        empty_profile = UserProfile()
        result = score_paper(sample_paper, empty_profile)
        assert result is None
