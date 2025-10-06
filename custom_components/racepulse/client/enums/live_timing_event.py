from enum import Enum
from typing import Optional


class LiveTimingEvent(str, Enum):
    """
    Enumeration of all supported Formula 1 live timing event types.

    Each enum member corresponds directly to the SignalR "Type"
    field in the raw event payload.

    Example:
        {
            "Type": "WeatherData",
            "DateTime": "2025-10-03T15:30:00Z",
            "Json": {
                "AirTemp": "28.5",
                "Humidity": "73.0",
                ...
            }
        }

    Usage:
        >>> LiveTimingEvent.WEATHER_DATA.value
        'WeatherData'
        >>> str(LiveTimingEvent.WEATHER_DATA)
        'WeatherData'
    """

    DRIVER_LIST = "DriverList"
    EXTRAPOLATED_CLOCK = "ExtrapolatedClock"
    HEARTBEAT = "Heartbeat"
    RACE_CONTROL_MESSAGES = "RaceControlMessages"
    SESSION_INFO = "SessionInfo"
    TEAM_RADIO = "TeamRadio"
    TIMING_APP = "TimingAppData"
    TIMING_STATS = "TimingStats"
    TIMING_DATA = "TimingData"
    TRACK_STATUS = "TrackStatus"
    WEATHER_DATA = "WeatherData"

    def __str__(self) -> str:
        """Return the raw event string (e.g. 'WeatherData')."""
        return self.value

    @classmethod
    def try_from(cls, value: str) -> Optional["LiveTimingEvent"]:
        """
        Attempt to create a LiveTimingEvent from a string.
        Returns None if the string doesn't match any known event type.

        Example:
            >>> LiveTimingEvent.try_from("WeatherData")
            <LiveTimingEvent.WEATHER_DATA: 'WeatherData'>
            >>> LiveTimingEvent.try_from("UnknownEvent")
            None
        """
        if not isinstance(value, str):
            return None
        try:
            return cls(value)
        except ValueError:
            return None