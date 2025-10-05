from typing import Callable, Dict, Type
from ..interfaces import Event
from ..enums import LiveTimingEvent

# Central event registry mapping event types to dataclass classes
_EVENT_REGISTRY: Dict[LiveTimingEvent, Type[Event]] = {}


def register_event(event_type: LiveTimingEvent) -> Callable[[Type[Event]], Type[Event]]:
    """
    Decorator for auto-registering a dataclass as the handler for a specific F1 Live Timing event.

    Example:
        @register_event(LiveTimingEvent.WEATHER)
        @dataclass(frozen=True)
        class WeatherData(Event):
            ...

    Args:
        event_type: The enum member from `LiveTimingEvent` representing this event type.

    Returns:
        A decorator that registers the dataclass into `_EVENT_REGISTRY`.
    """

    def _wrap(cls: Type[Event]) -> Type[Event]:
        # Warn if overwriting an existing registration
        if event_type in _EVENT_REGISTRY:
            existing = _EVENT_REGISTRY[event_type].__name__
            print(
                f"[register_event] Warning: Overwriting existing event '{event_type}' (was {existing})"
            )

        _EVENT_REGISTRY[event_type] = cls
        return cls

    return _wrap
