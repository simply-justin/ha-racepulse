from abc import ABC, abstractmethod
from typing import Any


class EventParser(ABC):
    """Base interface for all event parser."""

    @abstractmethod
    def supports(self, event_type: str) -> bool:
        """Return True if this mapper can handle the event type."""

    @abstractmethod
    def parse(self, raw: dict[str, Any]) -> object:
        """Convert raw JSON into a dataclass instance."""