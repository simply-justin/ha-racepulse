from typing import Any, Dict, Union, Type
from datetime import datetime, timezone
from .enums import LiveTimingEvent
from .interfaces import _PARSER_REGISTRY, EventParser, Event
from .models import RawTimingEvent


class EventFactory:
    """
    Resolves raw SignalR events into typed dataclasses using the registered parser registry.

    Each parser should be registered with:
        @register_parser(LiveTimingEvent.<EVENT_TYPE>)

    If no parser exists for the event type, or if parsing fails, this factory
    returns a fallback `RawTimingEvent` instance containing the raw payload.
    """

    @staticmethod
    def parse(event_type: LiveTimingEvent, raw: Dict[str, Any]) -> Union[Event, RawTimingEvent]:
        """
        Parse a raw SignalR event dictionary into a typed dataclass.

        Args:
            event_type: The `LiveTimingEvent` type representing this event.
            raw: The full event dictionary received from the SignalR stream.

        Returns:
            A parsed dataclass instance if a parser is registered and succeeds,
            otherwise a fallback `RawTimingEvent`.
        """
        parser_cls: Type[EventParser] | None = _PARSER_REGISTRY.get(event_type)

        # Build a fallback RawTimingEvent immediately
        raw_event = RawTimingEvent(
            event_type=event_type,
            payload=raw,
            datetime_utc=datetime.now(timezone.utc),
        )

        # Try to use a registered parser
        if parser_cls:
            parser = parser_cls()
            try:
                return parser.parse(raw_event)
            except Exception as ex:
                parser_name = parser_cls.__name__
                print(f"[EventFactory] ❌ Parser '{parser_name}' failed for {event_type}: {repr(ex)}")

        # Fallback: return the unparsed event wrapper
        return raw_event
