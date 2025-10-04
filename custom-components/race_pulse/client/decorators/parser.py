from typing import Callable, Dict, Type
from ..interfaces import EventParser

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