from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Type

# Global registry of parsers by event type string (e.g., "WeatherData")
_PARSER_REGISTRY: Dict[str, Type["EventParser"]] = {}


def register_parser(
    event_type: str,
) -> Callable[[Type["EventParser"]], Type["EventParser"]]:
    """
    Decorator to auto-register a parser class for a given SignalR 'Type' string.
    Open/Closed: new event = new class + decorator; no factory edits.
    """

    def _wrap(cls: Type["EventParser"]) -> Type["EventParser"]:
        _PARSER_REGISTRY[event_type] = cls
        return cls

    return _wrap


class EventParser(ABC):
    """Strategy interface: raw dict → typed dataclass."""

    @abstractmethod
    def parse(self, raw: Dict[str, Any]) -> object:
        """Convert raw JSON into a dataclass instance."""
        pass
