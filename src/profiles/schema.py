from dataclasses import dataclass, field


@dataclass
class UserProfile:
    """User research profile — describes what the user cares about."""

    topic_interests: list[str] = field(default_factory=list)
    required_signals: list[str] = field(default_factory=list)
    negative_filters: list[str] = field(default_factory=list)
    project_context: str = ""
    expertise_level: str = "intermediate"
