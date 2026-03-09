"""Tests for the config wizard."""

import json
from unittest.mock import patch

from src.cli.wizard import (
    _fallback_config,
    _generate_config,
    _parse_days_back,
    _validate_categories,
)
from src.core.config import LLMConfig


class TestValidateCategories:
    def test_keeps_valid_categories(self):
        config = {"sources": {"arxiv": {"categories": ["cs.LG", "hep-ex", "stat.ML"]}}}
        result = _validate_categories(config)
        assert result["sources"]["arxiv"]["categories"] == ["cs.LG", "hep-ex", "stat.ML"]

    def test_removes_invalid_categories(self):
        config = {"sources": {"arxiv": {"categories": ["cs.LG", "fake.XX", "hep-ex"]}}}
        result = _validate_categories(config)
        assert result["sources"]["arxiv"]["categories"] == ["cs.LG", "hep-ex"]

    def test_handles_empty_categories(self):
        config = {"sources": {"arxiv": {"categories": []}}}
        result = _validate_categories(config)
        assert result["sources"]["arxiv"]["categories"] == []

    def test_handles_missing_sources(self):
        config = {"profile": {}}
        result = _validate_categories(config)
        assert result == {"profile": {}}


class TestFallbackConfig:
    def test_basic_fallback(self):
        answers = {
            "field": "machine learning",
            "topics": "GNNs, transformers",
            "current": "new architectures for graph data",
            "level": "advanced",
            "avoid": "not specified",
        }
        config = _fallback_config(answers)
        assert config["profile"]["topic_interests"] == ["GNNs", "transformers"]
        assert config["profile"]["expertise_level"] == "advanced"
        assert config["sources"]["arxiv"]["enabled"] is True
        assert config["sources"]["inspire"]["enabled"] is False

    def test_fallback_uses_field_when_no_topics(self):
        answers = {"field": "neuroscience", "topics": "", "current": "", "level": "beginner", "avoid": ""}
        config = _fallback_config(answers)
        assert config["profile"]["topic_interests"] == ["neuroscience"]

    def test_fallback_normalizes_invalid_level(self):
        answers = {"field": "physics", "topics": "tracking", "current": "", "level": "guru", "avoid": ""}
        config = _fallback_config(answers)
        assert config["profile"]["expertise_level"] == "intermediate"


class TestParseDaysBack:
    def test_plain_integer(self):
        assert _parse_days_back("7") == 7
        assert _parse_days_back("30") == 30

    def test_days_unit(self):
        assert _parse_days_back("30 days") == 30
        assert _parse_days_back("1 day") == 1

    def test_weeks(self):
        assert _parse_days_back("2 weeks") == 14
        assert _parse_days_back("1 week") == 7

    def test_months(self):
        assert _parse_days_back("3 months") == 90
        assert _parse_days_back("1 month") == 30

    def test_years(self):
        assert _parse_days_back("1 year") == 365
        assert _parse_days_back("5 years") == 1825

    def test_empty_defaults_to_7(self):
        assert _parse_days_back("") == 7

    def test_garbage_defaults_to_7(self):
        assert _parse_days_back("forever") == 7


class TestGenerateConfig:
    @patch("src.cli.wizard.call_llm")
    def test_generates_valid_config(self, mock_llm):
        mock_llm.return_value = json.dumps({
            "profile": {
                "topic_interests": ["graph neural networks", "particle tracking"],
                "required_signals": ["benchmark"],
                "negative_filters": ["survey only"],
                "project_context": "Working on GNNs for tracking.",
                "expertise_level": "advanced",
            },
            "sources": {
                "arxiv": {"enabled": True, "categories": ["cs.LG", "hep-ex"], "max_results": 50},
                "inspire": {"enabled": True, "keywords": ["tracking"], "subject_codes": ["Experiment-HEP"]},
            },
        })
        answers = {
            "field": "ML", "topics": "GNNs", "current": "tracking",
            "signals": "benchmark", "level": "advanced", "avoid": "",
            "days_back": "7",
        }
        result = _generate_config(answers, LLMConfig())
        assert result is not None
        assert "profile" in result
        assert "sources" in result

    @patch("src.cli.wizard.call_llm")
    def test_returns_none_on_bad_json(self, mock_llm):
        mock_llm.return_value = "not valid json"
        answers = {
            "field": "ML", "topics": "GNNs", "current": "",
            "signals": "", "level": "advanced", "avoid": "",
            "days_back": "7",
        }
        result = _generate_config(answers, LLMConfig())
        assert result is None

    @patch("src.cli.wizard.call_llm")
    def test_returns_none_on_missing_keys(self, mock_llm):
        mock_llm.return_value = json.dumps({"wrong_key": "value"})
        answers = {
            "field": "ML", "topics": "GNNs", "current": "",
            "signals": "", "level": "advanced", "avoid": "",
            "days_back": "7",
        }
        result = _generate_config(answers, LLMConfig())
        assert result is None
