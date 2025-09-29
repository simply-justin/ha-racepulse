from abc import ABC, abstractmethod
from typing import Any, Dict


class EventParser(ABC):
    """Base interface for all event parser."""

    @abstractmethod
    def supports(self, event_type: str) -> bool:
        """Return True if this mapper can handle the event type."""
        pass

    @abstractmethod
    def parse(self, raw: Dict[str, Any]) -> object:
        """Convert raw JSON into a dataclass instance."""
        pass