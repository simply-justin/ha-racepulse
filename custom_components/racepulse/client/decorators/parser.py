from typing import Callable, Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ..enums import LiveTimingEvent
    from ..interfaces import EventParser

# Global registry for parser classes keyed by their LiveTimingEvent type
_PARSER_REGISTRY: Dict["LiveTimingEvent", Type["EventParser"]] = {}


def register_parser(
    event_type: "LiveTimingEvent",
) -> Callable[[Type["EventParser"]], Type["EventParser"]]:
    """
    Decorator to register an EventParser class for a given LiveTimingEvent type.

    Example:
        @register_parser(LiveTimingEvent.WEATHER)
        class WeatherDataParser(EventParser[WeatherData]):
            def parse(self, raw: RawTimingEvent) -> WeatherData:
                ...

    This system allows new event parsers to be added without modifying the factory:
    simply define a new parser and apply the decorator.

    Args:
        event_type: A member of the `LiveTimingEvent` enum representing the event to handle.

    Returns:
        The same class, after registration.
    """

    def _wrap(cls: Type["EventParser"]) -> Type["EventParser"]:
        # Ensure valid subclass
        from ..interfaces import EventParser

        if not issubclass(cls, EventParser):
            raise TypeError(
                f"@register_parser({event_type}) can only be applied to subclasses of EventParser, got {cls.__name__}"
            )

        # Warn if overwriting an existing parser
        if event_type in _PARSER_REGISTRY:
            existing = _PARSER_REGISTRY[event_type].__name__
            print(
                f"[register_parser] Warning: Overwriting existing parser for {event_type} (was {existing})"
            )

        _PARSER_REGISTRY[event_type] = cls
        return cls

    return _wrap
