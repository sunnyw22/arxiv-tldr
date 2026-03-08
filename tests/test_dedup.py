"""Tests for deduplication, profile hash, and score reuse logic."""

import pytest

from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import RankedPaper
from src.storage.sqlite import get_connection, save_papers, save_run
from src.workflows.daily_digest import _dedup_papers, _load_previous_scores, profile_hash
from tests.conftest import make_paper


class TestDedupPapers:
    def test_no_duplicates(self):
        papers = [make_paper("id-1"), make_paper("id-2")]
        result = _dedup_papers(papers)
        assert len(result) == 2

    def test_exact_source_id_dedup(self):
        papers = [make_paper("id-1"), make_paper("id-1")]
        result = _dedup_papers(papers)
        assert len(result) == 1

    def test_arxiv_version_stripping(self):
        """2603.01234v1 and 2603.01234v2 should dedup to one paper."""
        papers = [
            make_paper("2603.01234v1", source_type="arxiv_api"),
            make_paper("2603.01234v2", source_type="arxiv_api"),
        ]
        result = _dedup_papers(papers)
        assert len(result) == 1
        assert result[0].source_id == "2603.01234v1"  # first one wins

    def test_inspire_arxiv_crossref_dedup(self):
        """INSPIRE paper with arxiv_id in raw_metadata should dedup against arXiv paper."""
        arxiv_paper = make_paper("2603.01234v1", source_type="arxiv_api")
        inspire_paper = make_paper(
            "inspire-123",
            source_type="inspire",
            raw_metadata={"arxiv_id": "2603.01234v1"},
        )
        result = _dedup_papers([arxiv_paper, inspire_paper])
        assert len(result) == 1

    def test_different_papers_preserved(self):
        papers = [
            make_paper("2603.01111v1", source_type="arxiv_api"),
            make_paper("2603.02222v1", source_type="arxiv_api"),
            make_paper("inspire-999", source_type="inspire"),
        ]
        result = _dedup_papers(papers)
        assert len(result) == 3

    def test_empty_list(self):
        assert _dedup_papers([]) == []

    def test_arxiv_rss_type_dedup(self):
        """arxiv_rss source type should also strip versions."""
        papers = [
            make_paper("2603.01234v1", source_type="arxiv_rss"),
            make_paper("2603.01234v2", source_type="arxiv_rss"),
        ]
        result = _dedup_papers(papers)
        assert len(result) == 1


class TestProfileHash:
    def test_same_profile_same_hash(self):
        p1 = UserProfile(topic_interests=["ML"], project_context="My project", expertise_level="expert")
        p2 = UserProfile(topic_interests=["ML"], project_context="My project", expertise_level="expert")
        assert profile_hash(p1) == profile_hash(p2)

    def test_different_interests_different_hash(self):
        p1 = UserProfile(topic_interests=["ML"])
        p2 = UserProfile(topic_interests=["NLP"])
        assert profile_hash(p1) != profile_hash(p2)

    def test_different_context_different_hash(self):
        p1 = UserProfile(project_context="Project A")
        p2 = UserProfile(project_context="Project B")
        assert profile_hash(p1) != profile_hash(p2)

    def test_different_expertise_different_hash(self):
        p1 = UserProfile(expertise_level="beginner")
        p2 = UserProfile(expertise_level="expert")
        assert profile_hash(p1) != profile_hash(p2)

    def test_order_independent_interests(self):
        """topic_interests are sorted before hashing."""
        p1 = UserProfile(topic_interests=["B", "A"])
        p2 = UserProfile(topic_interests=["A", "B"])
        assert profile_hash(p1) == profile_hash(p2)

    def test_hash_excludes_required_signals_and_negative_filters(self):
        """required_signals and negative_filters are intentionally excluded from the hash.

        These fields only affect the pre-sort stage (keyword scoring and hard rejection),
        not the LLM scoring prompt. Papers rejected by negative_filters are never scored,
        so they have no cached scores to go stale. When filters change, rejected papers
        simply re-enter the pre-sort with the new config and get evaluated fresh.

        The LLM prompt only uses: topic_interests, project_context, expertise_level.
        The hash correctly covers exactly those fields.
        """
        p1 = UserProfile(topic_interests=["ML"], required_signals=["ATLAS"])
        p2 = UserProfile(topic_interests=["ML"], required_signals=["CMS"])
        assert profile_hash(p1) == profile_hash(p2)

        p3 = UserProfile(topic_interests=["ML"], negative_filters=["survey"])
        p4 = UserProfile(topic_interests=["ML"], negative_filters=["robotics"])
        assert profile_hash(p3) == profile_hash(p4)


class TestScoreReuse:
    """Tests that score caching interacts correctly with negative_filters.

    Key invariant: papers rejected by negative_filters are never LLM-scored,
    so they have no cached scores. When filters change, these papers naturally
    flow into needs_scoring and get evaluated fresh with the current config.
    """

    @pytest.fixture
    def db_conn(self, tmp_path):
        conn = get_connection(tmp_path / "test.db")
        yield conn
        conn.close()

    def test_negative_filtered_paper_has_no_cached_score(self, db_conn):
        """A paper that was rejected by negative_filters in run 1
        should NOT appear in reused scores for run 2."""
        scored_paper = make_paper("id-scored", "Good Paper")
        filtered_paper = make_paper("id-filtered", "Survey Only: Bad Paper")
        save_papers(db_conn, [scored_paper, filtered_paper])

        # Run 1: only scored_paper was LLM-scored; filtered_paper was rejected at pre-sort
        profile = UserProfile(topic_interests=["ML"], negative_filters=["survey only"])
        current_hash = profile_hash(profile)
        ranked = [RankedPaper(paper=scored_paper, relevance_score=8, reasoning="R", summary="S")]
        save_run(db_conn, ranked, total_fetched=2, config_snapshot={"profile_hash": current_hash})

        # Run 2: same profile, both papers in current fetch
        both_papers = [scored_paper, filtered_paper]
        reused = _load_previous_scores(db_conn, current_hash, both_papers)

        # scored_paper should be reused, filtered_paper should NOT (it was never scored)
        reused_ids = {rp.paper.source_id for rp in reused}
        assert "id-scored" in reused_ids
        assert "id-filtered" not in reused_ids

    def test_removing_negative_filter_allows_rescoring(self, db_conn):
        """When a negative filter is removed, previously-rejected papers
        have no cached scores, so they naturally go to needs_scoring."""
        scored_paper = make_paper("id-scored", "Good Paper")
        filtered_paper = make_paper("id-filtered", "Survey Only: Filtered Paper")
        save_papers(db_conn, [scored_paper, filtered_paper])

        # Run 1: with negative filter, only scored_paper was ranked
        profile_v1 = UserProfile(topic_interests=["ML"], negative_filters=["survey only"])
        hash_v1 = profile_hash(profile_v1)
        ranked = [RankedPaper(paper=scored_paper, relevance_score=8, reasoning="R", summary="S")]
        save_run(db_conn, ranked, total_fetched=2, config_snapshot={"profile_hash": hash_v1})

        # Run 2: negative filter removed — but hash is the same (filters not in hash)
        profile_v2 = UserProfile(topic_interests=["ML"], negative_filters=[])
        hash_v2 = profile_hash(profile_v2)
        assert hash_v1 == hash_v2  # same hash since LLM-affecting fields unchanged

        both_papers = [scored_paper, filtered_paper]
        reused = _load_previous_scores(db_conn, hash_v2, both_papers)

        # scored_paper reused, filtered_paper has no cached score → goes to needs_scoring
        reused_ids = {rp.paper.source_id for rp in reused}
        assert "id-scored" in reused_ids
        assert "id-filtered" not in reused_ids
        # filtered_paper would then hit pre-sort with no negative filter → pass → LLM scored

    def test_profile_change_invalidates_all_cached_scores(self, db_conn):
        """Changing topic_interests (which IS in the hash) invalidates all cached scores."""
        paper = make_paper("id-1", "Some Paper")
        save_papers(db_conn, [paper])

        profile_v1 = UserProfile(topic_interests=["ML"])
        hash_v1 = profile_hash(profile_v1)
        ranked = [RankedPaper(paper=paper, relevance_score=8, reasoning="R", summary="S")]
        save_run(db_conn, ranked, total_fetched=1, config_snapshot={"profile_hash": hash_v1})

        # Change topic_interests → different hash → all scores invalidated
        profile_v2 = UserProfile(topic_interests=["NLP"])
        hash_v2 = profile_hash(profile_v2)
        assert hash_v1 != hash_v2

        reused = _load_previous_scores(db_conn, hash_v2, [paper])
        assert reused == []  # nothing reused, everything re-scored
