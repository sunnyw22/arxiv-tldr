from abc import ABC, abstractmethod

from src.core.models import Paper


class BaseSource(ABC):
    """Protocol for paper sources."""

    @abstractmethod
    def fetch(self, **kwargs) -> list[Paper]:
        """Fetch papers and return normalized Paper records."""
        ...
