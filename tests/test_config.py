"""Tests for config loading and parsing."""


import pytest
import yaml

from src.core.config import AppConfig, _parse_config, load_config


class TestParseConfig:
    def test_empty_config_returns_defaults(self):
        config = _parse_config({})
        assert config.llm.model == "openai/gpt-4o-mini"
        assert config.summary.max_papers == 10
        assert config.output.formats == ["markdown"]
        assert config.profile.expertise_level == "intermediate"
        assert config.sources.arxiv.enabled is True

    def test_full_config(self):
        raw = {
            "profile": {
                "topic_interests": ["ML", "tracking"],
                "required_signals": ["ATLAS"],
                "negative_filters": ["survey only"],
                "project_context": "My project",
                "expertise_level": "expert",
            },
            "sources": {
                "arxiv": {"enabled": True, "categories": ["hep-ex"]},
                "inspire": {"enabled": False, "keywords": ["jets"]},
            },
            "summary": {"style": "detailed", "max_papers": 5},
            "output": {"formats": ["markdown", "html"], "output_dir": "reports/"},
            "llm": {"model": "openai/gpt-4o-mini", "temperature": 0.5, "max_tokens": 2048},
        }
        config = _parse_config(raw)
        assert config.profile.topic_interests == ["ML", "tracking"]
        assert config.profile.expertise_level == "expert"
        assert config.sources.arxiv.categories == ["hep-ex"]
        assert config.sources.inspire.enabled is False
        assert config.summary.max_papers == 5
        assert config.output.output_dir == "reports/"
        assert config.llm.model == "openai/gpt-4o-mini"

    def test_partial_config_fills_defaults(self):
        raw = {"profile": {"topic_interests": ["NLP"]}}
        config = _parse_config(raw)
        assert config.profile.topic_interests == ["NLP"]
        assert config.profile.negative_filters == []
        assert config.llm.temperature == 0.3

    def test_project_context_whitespace_stripped(self):
        raw = {"profile": {"project_context": "  my context  \n "}}
        config = _parse_config(raw)
        assert config.profile.project_context == "my context"


class TestLoadConfig:
    def test_load_valid_yaml(self, tmp_path):
        config_file = tmp_path / "config.yaml"
        config_file.write_text(yaml.dump({
            "profile": {"topic_interests": ["transformers"]},
            "llm": {"model": "test/model"},
        }))
        config = load_config(config_file)
        assert config.profile.topic_interests == ["transformers"]
        assert config.llm.model == "test/model"

    def test_load_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            load_config("/nonexistent/config.yaml")

    def test_load_empty_yaml(self, tmp_path):
        config_file = tmp_path / "empty.yaml"
        config_file.write_text("")
        config = load_config(config_file)
        assert isinstance(config, AppConfig)
        assert config.profile.topic_interests == []
