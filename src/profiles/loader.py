from pathlib import Path

from src.core.config import load_config
from src.profiles.schema import UserProfile


def load_profile(config_path: str | Path = "config/config.yaml") -> UserProfile:
    """Load user profile from config file."""
    config = load_config(config_path)
    return config.profile
