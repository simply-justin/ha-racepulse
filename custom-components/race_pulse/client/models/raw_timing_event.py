from dataclasses import dataclass
from datetime import datetime
from typing import Any, Final
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class RawTimingEvent:
    """
    Represents a raw live timing event as received directly from the Formula 1 Live Timing feed.

    This class stores the unparsed payload data, along with the event type and timestamp
    indicating when the event was emitted by the F1 feed. It serves as the lowest-level
    abstraction before parsing into structured event dataclasses (e.g., `DriverList`, `Heartbeat`).

    Attributes:
        event_type: The type of live timing event (e.g., `LiveTimingEvent.TIMING_DATA`,
                    `LiveTimingEvent.WEATHER_DATA`, etc.).
        payload: The raw JSON payload content as received, typically a dictionary.
        datetime_utc: The UTC timestamp when the event was emitted.
    """

    event_type: Final[LiveTimingEvent]
    payload: Any
    datetime_utc: datetime
