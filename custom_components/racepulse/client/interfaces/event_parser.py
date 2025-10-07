from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from ..models import RawTimingEvent

T = TypeVar("T")


class EventParser(ABC, Generic[T]):
    """
    Abstract base class for all event parsers.

    Each parser converts a `RawTimingEvent` into a typed dataclass
    (such as `DriverList`, `TimingData`, or `WeatherData`).

    Parsers are registered automatically via the `@register_parser` decorator,
    which associates them with a specific `LiveTimingEvent` type.
    """

    @abstractmethod
    def parse(self, raw: RawTimingEvent) -> T:
        """
        Convert a raw timing event into its typed dataclass form.

        Args:
            raw: A `RawTimingEvent` containing the event type, UTC timestamp,
                 and raw JSON payload.

        Returns:
            A parsed dataclass instance representing this event type.
        """
        raise NotImplementedError
