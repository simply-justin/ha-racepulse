from abc import ABC, abstractmethod
from typing import Any, Dict


class EventParser(ABC):
    """Strategy interface: raw dict → typed dataclass."""

    @abstractmethod
    def parse(self, raw: Dict[str, Any]) -> object:
        """Convert raw JSON into a dataclass instance."""
        pass
