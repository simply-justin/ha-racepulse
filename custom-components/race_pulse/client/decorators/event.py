from typing import Callable, Dict, Type
from ..interfaces import Event

_EVENT_REGISTRY: Dict[str, Type["Event"]] = {}

def register_event(
    event_type: str,
) -> Callable[[Type["Event"]], Type["Event"]]:
    """
    Decorator to auto-register a event class for a given SignalR 'Type' string.
    """

    def _wrap(cls: Type["Event"]) -> Type["Event"]:
        _EVENT_REGISTRY[event_type] = cls
        return cls

    return _wrap