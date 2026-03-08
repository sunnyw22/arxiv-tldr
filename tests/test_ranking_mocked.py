"""Tests for LLM ranking and synonym expansion with mocked LLM calls."""

import json
from unittest.mock import patch

from src.core.config import LLMConfig
from src.profiles.schema import UserProfile
from src.ranking.rerank_llm import rerank_and_summarize
from src.ranking.synonym import expand_keywords
from tests.conftest import make_paper


class TestExpandKeywords:
    @patch("src.ranking.synonym.call_llm")
    def test_expand_returns_terms(self, mock_llm):
        mock_llm.return_value = json.dumps({
            "expanded_terms": ["ML", "machine learning", "deep learning", "neural networks"]
        })
        profile = UserProfile(topic_interests=["machine learning"])
        config = LLMConfig()
        result = expand_keywords(profile, config)
        assert "ML" in result
        assert "deep learning" in result

    @patch("src.ranking.synonym.call_llm")
    def test_expand_deduplicates(self, mock_llm):
        mock_llm.return_value = json.dumps({
            "expanded_terms": ["ML", "ml", "Machine Learning", "ML"]
        })
        profile = UserProfile(topic_interests=["ML"])
        result = expand_keywords(profile, LLMConfig())
        # Should deduplicate case-insensitively
        assert len(result) == 2  # "ML" and "Machine Learning"

    @patch("src.ranking.synonym.call_llm")
    def test_expand_fallback_on_bad_json(self, mock_llm):
        mock_llm.return_value = "not valid json"
        profile = UserProfile(topic_interests=["ML", "tracking"])
        result = expand_keywords(profile, LLMConfig())
        assert result == ["ML", "tracking"]  # falls back to original

    def test_expand_empty_profile(self):
        profile = UserProfile()
        result = expand_keywords(profile, LLMConfig())
        assert result == []


class TestRerankAndSummarize:
    @patch("src.ranking.rerank_llm.call_llm")
    def test_ranks_and_sorts(self, mock_llm):
        papers = [make_paper("id-1", "Relevant Paper"), make_paper("id-2", "Less Relevant")]
        mock_llm.return_value = json.dumps({
            "papers": [
                {
                    "paper_id": "id-1", "relevance_score": 8,
                    "reasoning": "Great match",
                    "abstract_takeaway": "Presents a new ML method.",
                    "why_relevant": "Directly useful for your project.",
                    "summary": "Summary 1",
                },
                {
                    "paper_id": "id-2", "relevance_score": 3,
                    "reasoning": "Poor match",
                    "abstract_takeaway": "Studies quantum effects.",
                    "why_relevant": "Limited overlap with your work.",
                    "summary": "Summary 2",
                },
            ]
        })
        profile = UserProfile(topic_interests=["ML"])
        result = rerank_and_summarize(papers, profile, LLMConfig(), top_n=10)
        assert len(result) == 2
        assert result[0].relevance_score == 8
        assert result[1].relevance_score == 3
        assert result[0].abstract_takeaway == "Presents a new ML method."
        assert result[0].why_relevant == "Directly useful for your project."

    @patch("src.ranking.rerank_llm.call_llm")
    def test_new_fields_default_empty(self, mock_llm):
        """When LLM response omits new fields, they default to empty strings."""
        papers = [make_paper("id-1", "Paper")]
        mock_llm.return_value = json.dumps({
            "papers": [
                {"paper_id": "id-1", "relevance_score": 7, "reasoning": "Good", "summary": "S"},
            ]
        })
        result = rerank_and_summarize(papers, UserProfile(), LLMConfig(), top_n=10)
        assert result[0].abstract_takeaway == ""
        assert result[0].why_relevant == ""

    @patch("src.ranking.rerank_llm.call_llm")
    def test_top_n_cutoff(self, mock_llm):
        papers = [make_paper(f"id-{i}") for i in range(5)]
        mock_llm.return_value = json.dumps({
            "papers": [
                {"paper_id": f"id-{i}", "relevance_score": 10 - i, "reasoning": "R", "summary": "S"}
                for i in range(5)
            ]
        })
        result = rerank_and_summarize(papers, UserProfile(), LLMConfig(), top_n=3)
        assert len(result) == 3
        assert all(r.relevance_score >= 8 for r in result)

    @patch("src.ranking.rerank_llm.call_llm")
    def test_tie_inclusive_cutoff(self, mock_llm):
        papers = [make_paper(f"id-{i}") for i in range(4)]
        mock_llm.return_value = json.dumps({
            "papers": [
                {"paper_id": "id-0", "relevance_score": 9, "reasoning": "R", "summary": "S"},
                {"paper_id": "id-1", "relevance_score": 7, "reasoning": "R", "summary": "S"},
                {"paper_id": "id-2", "relevance_score": 7, "reasoning": "R", "summary": "S"},
                {"paper_id": "id-3", "relevance_score": 5, "reasoning": "R", "summary": "S"},
            ]
        })
        result = rerank_and_summarize(papers, UserProfile(), LLMConfig(), top_n=2)
        # top_n=2 but score at position 2 is 7, which ties with position 3 → include both
        assert len(result) == 3
        scores = [r.relevance_score for r in result]
        assert 5 not in scores

    @patch("src.ranking.rerank_llm.call_llm")
    def test_invalid_json_graceful(self, mock_llm):
        mock_llm.return_value = "not json at all"
        papers = [make_paper("id-1")]
        result = rerank_and_summarize(papers, UserProfile(), LLMConfig())
        assert len(result) == 1
        assert result[0].relevance_score == 0

    @patch("src.ranking.rerank_llm.call_llm")
    def test_batching(self, mock_llm):
        """Papers are processed in batches."""
        papers = [make_paper(f"id-{i}") for i in range(15)]

        def mock_response(*args, **kwargs):
            # Return valid response for whatever batch is sent
            return json.dumps({
                "papers": [
                    {"paper_id": p.source_id, "relevance_score": 5, "reasoning": "R", "summary": "S"}
                    for p in papers[:10]  # won't match exactly but position fallback handles it
                ]
            })

        mock_llm.side_effect = mock_response
        rerank_and_summarize(papers, UserProfile(), LLMConfig(), batch_size=10)
        assert mock_llm.call_count == 2  # 15 papers / batch_size 10 = 2 calls
