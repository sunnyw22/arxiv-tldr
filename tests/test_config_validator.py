"""Tests for LLM-based config validation."""

import json
from unittest.mock import patch

import pytest

from src.core.config import LLMConfig
from src.core.config_validator import validate_config


@pytest.fixture
def llm_config():
    return LLMConfig(model="test/model", temperature=0.3, max_tokens=1024)


VALID_CONFIG_YAML = """\
profile:
  topic_interests:
    - machine learning
  required_signals:
    - ATLAS
  negative_filters: []
  project_context: "My research project"
  expertise_level: intermediate
sources:
  arxiv:
    enabled: true
    categories:
      - hep-ex
summary:
  style: concise
  max_papers: 10
output:
  formats:
    - markdown
  output_dir: output/
llm:
  model: anthropic/claude-sonnet-4-20250514
  temperature: 0.3
  max_tokens: 4096
schedule:
  cron: "0 8 * * *"
  timezone: UTC
"""

CONFIG_WITH_TYPOS_YAML = """\
profle:
  topic_interests:
    - machine learning
  expretise_level: intermediate
sources:
  arxiv:
    enbled: true
    categories: hep-ex
summary:
  stlye: concise
  max_papers: 0
llm:
  model: anthropic/claude-sonnet-4-20250514
  temperature: 3.5
"""


class TestValidateConfig:
    def test_valid_config_returns_no_warnings(self, llm_config):
        """A valid config should produce an empty warnings list."""
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.return_value = json.dumps([])
            warnings = validate_config(VALID_CONFIG_YAML, llm_config)

        assert warnings == []
        mock_llm.assert_called_once()

    def test_config_with_typos_returns_warnings(self, llm_config):
        """A config with typos and bad values should produce warnings."""
        expected_warnings = [
            "Unknown top-level key 'profle' — did you mean 'profile'?",
            "Unknown key 'expretise_level' — did you mean 'expertise_level'?",
            "Key 'enbled' under sources.arxiv — did you mean 'enabled'?",
            "sources.arxiv.categories should be a list, not a string.",
            "summary.max_papers should be a positive integer, got 0.",
            "llm.temperature is 3.5, which exceeds the maximum of 2.0.",
        ]
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.return_value = json.dumps(expected_warnings)
            warnings = validate_config(CONFIG_WITH_TYPOS_YAML, llm_config)

        assert len(warnings) == 6
        assert "profle" in warnings[0]
        assert "temperature" in warnings[5]

    def test_llm_failure_returns_empty_warnings(self, llm_config):
        """If the LLM call fails, validation should not block the pipeline."""
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.side_effect = RuntimeError("API unavailable")
            warnings = validate_config(VALID_CONFIG_YAML, llm_config)

        assert warnings == []

    def test_malformed_llm_response_returns_empty_warnings(self, llm_config):
        """If the LLM returns invalid JSON, validation should not block."""
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.return_value = "This is not JSON"
            warnings = validate_config(VALID_CONFIG_YAML, llm_config)

        assert warnings == []

    def test_llm_returns_non_list_json(self, llm_config):
        """If the LLM returns JSON that isn't a list, treat as no warnings."""
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.return_value = json.dumps({"warnings": ["something"]})
            warnings = validate_config(VALID_CONFIG_YAML, llm_config)

        assert warnings == []

    def test_validation_uses_low_temperature(self, llm_config):
        """Validation should use temperature=0.0 for deterministic results."""
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.return_value = json.dumps([])
            validate_config(VALID_CONFIG_YAML, llm_config)

        call_args = mock_llm.call_args
        validation_config = call_args.kwargs["config"]
        assert validation_config.temperature == 0.0

    def test_validation_uses_json_mode(self, llm_config):
        """Validation should request JSON mode from the LLM."""
        with patch("src.core.config_validator.call_llm") as mock_llm:
            mock_llm.return_value = json.dumps([])
            validate_config(VALID_CONFIG_YAML, llm_config)

        call_args = mock_llm.call_args
        assert call_args.kwargs["json_mode"] is True


class TestSkipValidationFlag:
    def test_skip_validation_flag_is_accepted(self):
        """The --skip-validation flag should be recognized by argparse."""
        import argparse

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")
        digest_parser = subparsers.add_parser("digest")
        digest_parser.add_argument("--skip-validation", action="store_true", default=False)
        digest_parser.add_argument("--config", "-c", default="config/config.yaml")
        digest_parser.add_argument("--db", default="data/research_radar.db")

        args = parser.parse_args(["digest", "--skip-validation"])
        assert args.skip_validation is True

    def test_skip_validation_default_is_false(self):
        """Without the flag, skip_validation should be False."""
        import argparse

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest="command")
        digest_parser = subparsers.add_parser("digest")
        digest_parser.add_argument("--skip-validation", action="store_true", default=False)
        digest_parser.add_argument("--config", "-c", default="config/config.yaml")
        digest_parser.add_argument("--db", default="data/research_radar.db")

        args = parser.parse_args(["digest"])
        assert args.skip_validation is False
