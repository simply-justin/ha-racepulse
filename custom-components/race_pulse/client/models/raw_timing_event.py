from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RawTimingEvent:
    """
    A raw live timing event as received from the F1 feed.

    Attributes:
        event_type: Type of event (e.g., "TimingData", "LapCount", "WeatherData").
        payload: Raw JSON payload (unparsed).
        timestamp_utc: UTC timestamp when the event was emitted.
    """

    event_type: str
    payload: Any
    timestamp_utc: datetime
