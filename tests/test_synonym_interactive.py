"""Tests for interactive synonym expansion."""

import json
from unittest.mock import patch

from src.core.config import LLMConfig
from src.profiles.schema import UserProfile
from src.ranking.synonym import expand_keywords_interactive


class TestExpandKeywordsInteractive:
    @patch("src.ranking.synonym.call_llm")
    @patch("builtins.input", return_value="a")
    def test_accept_all(self, mock_input, mock_llm):
        mock_llm.return_value = json.dumps({
            "expanded_terms": ["ML", "deep learning", "neural nets"]
        })
        profile = UserProfile(topic_interests=["machine learning"])
        result = expand_keywords_interactive(profile, LLMConfig())
        assert "machine learning" in result
        assert "ML" in result
        assert "deep learning" in result

    @patch("src.ranking.synonym.call_llm")
    @patch("builtins.input", return_value="s")
    def test_skip_expansion(self, mock_input, mock_llm):
        mock_llm.return_value = json.dumps({
            "expanded_terms": ["ML", "deep learning", "neural nets"]
        })
        profile = UserProfile(topic_interests=["machine learning"])
        result = expand_keywords_interactive(profile, LLMConfig())
        assert result == ["machine learning"]

    @patch("src.ranking.synonym.call_llm")
    @patch("builtins.input", side_effect=["e", "deep learning, neural nets", "a"])
    def test_edit_removes_terms(self, mock_input, mock_llm):
        mock_llm.return_value = json.dumps({
            "expanded_terms": ["ML", "deep learning", "neural nets"]
        })
        profile = UserProfile(topic_interests=["machine learning"])
        result = expand_keywords_interactive(profile, LLMConfig())
        assert "machine learning" in result
        assert "ML" in result
        assert "deep learning" not in result
        assert "neural nets" not in result

    @patch("src.ranking.synonym.call_llm")
    @patch("builtins.input", side_effect=["e", "machine learning", "a"])
    def test_edit_protects_original_interests(self, mock_input, mock_llm):
        mock_llm.return_value = json.dumps({
            "expanded_terms": ["ML", "deep learning"]
        })
        profile = UserProfile(topic_interests=["machine learning"])
        result = expand_keywords_interactive(profile, LLMConfig())
        # Original interest should not be removable
        assert "machine learning" in result

    @patch("src.ranking.synonym.call_llm")
    @patch("builtins.input", side_effect=["r", "a"])
    def test_regenerate(self, mock_input, mock_llm):
        # First call returns one set, second call returns another
        mock_llm.side_effect = [
            json.dumps({"expanded_terms": ["ML", "deep learning"]}),
            json.dumps({"expanded_terms": ["AI", "transformers"]}),
        ]
        profile = UserProfile(topic_interests=["machine learning"])
        result = expand_keywords_interactive(profile, LLMConfig())
        # Should use the regenerated set
        assert "AI" in result or "transformers" in result

    def test_empty_profile_returns_empty(self):
        profile = UserProfile()
        result = expand_keywords_interactive(profile, LLMConfig())
        assert result == []
