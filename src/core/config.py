from dataclasses import dataclass, field
from pathlib import Path

import yaml

from src.profiles.schema import UserProfile


@dataclass
class ArxivSourceConfig:
    enabled: bool = True
    categories: list[str] = field(default_factory=list)
    max_results: int = 50


@dataclass
class InspireSourceConfig:
    enabled: bool = True
    keywords: list[str] = field(default_factory=list)
    subject_codes: list[str] = field(default_factory=list)
    max_results: int = 50


@dataclass
class SourcesConfig:
    arxiv: ArxivSourceConfig = field(default_factory=ArxivSourceConfig)
    inspire: InspireSourceConfig = field(default_factory=InspireSourceConfig)


@dataclass
class SummaryConfig:
    style: str = "concise"
    max_papers: int = 15


@dataclass
class OutputConfig:
    formats: list[str] = field(default_factory=lambda: ["markdown"])
    output_dir: str = "output/"


@dataclass
class LLMConfig:
    model: str = "openai/gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 4096


@dataclass
class ScheduleConfig:
    cron: str = "0 8 * * *"
    timezone: str = "UTC"


@dataclass
class AppConfig:
    profile: UserProfile = field(default_factory=UserProfile)
    sources: SourcesConfig = field(default_factory=SourcesConfig)
    summary: SummaryConfig = field(default_factory=SummaryConfig)
    output: OutputConfig = field(default_factory=OutputConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    schedule: ScheduleConfig = field(default_factory=ScheduleConfig)


def load_config(path: str | Path = "config/config.yaml") -> AppConfig:
    """Load config from a YAML file and return a typed AppConfig."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path) as f:
        raw = yaml.safe_load(f) or {}

    return _parse_config(raw)


def _parse_config(raw: dict) -> AppConfig:
    """Parse raw YAML dict into typed AppConfig."""
    profile_raw = raw.get("profile", {})
    profile = UserProfile(
        topic_interests=profile_raw.get("topic_interests", []),
        required_signals=profile_raw.get("required_signals", []),
        negative_filters=profile_raw.get("negative_filters", []),
        project_context=profile_raw.get("project_context", "").strip(),
        expertise_level=profile_raw.get("expertise_level", "intermediate"),
    )

    sources_raw = raw.get("sources", {})
    arxiv_raw = sources_raw.get("arxiv", {})
    inspire_raw = sources_raw.get("inspire", {})
    sources = SourcesConfig(
        arxiv=ArxivSourceConfig(
            enabled=arxiv_raw.get("enabled", True),
            categories=arxiv_raw.get("categories", []),
            max_results=arxiv_raw.get("max_results", 50),
        ),
        inspire=InspireSourceConfig(
            enabled=inspire_raw.get("enabled", True),
            keywords=inspire_raw.get("keywords", []),
            subject_codes=inspire_raw.get("subject_codes", []),
            max_results=inspire_raw.get("max_results", 50),
        ),
    )

    summary_raw = raw.get("summary", {})
    summary = SummaryConfig(
        style=summary_raw.get("style", "concise"),
        max_papers=summary_raw.get("max_papers", 15),
    )

    output_raw = raw.get("output", {})
    output = OutputConfig(
        formats=output_raw.get("formats", ["markdown"]),
        output_dir=output_raw.get("output_dir", "output/"),
    )

    llm_raw = raw.get("llm", {})
    llm = LLMConfig(
        model=llm_raw.get("model", "openai/gpt-4o-mini"),
        temperature=llm_raw.get("temperature", 0.3),
        max_tokens=llm_raw.get("max_tokens", 1024),
    )

    schedule_raw = raw.get("schedule", {})
    schedule = ScheduleConfig(
        cron=schedule_raw.get("cron", "0 8 * * *"),
        timezone=schedule_raw.get("timezone", "UTC"),
    )

    return AppConfig(
        profile=profile,
        sources=sources,
        summary=summary,
        output=output,
        llm=llm,
        schedule=schedule,
    )
