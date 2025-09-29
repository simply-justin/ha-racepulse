from enum import Enum
from typing import Optional, Type

from ..models import (
    Car,
    ChampionshipPrediction,
    DriverList,
    ExtrapolatedClock,
    Heartbeat,
    LapCount,
    PositionData,
    RaceControlMessages,
    SessionInfo,
    TeamRadio,
    TimingApp,
    TimingStats,
    Timing,
    TrackStatus,
    Weather,
    PitStopSeries,
    PitLaneTimeCollection,
)


class LiveTimingEvent(Enum):
    """
    Enumeration of all supported live timing events.
    Each enum value is linked to its corresponding model class.
    """

    CAR_DATA = ("CarData", Car)
    CHAMPIONSHIP_PREDICTION = ("ChampionshipPrediction", ChampionshipPrediction)
    DRIVER_LIST = ("DriverList", DriverList)
    EXTRAPOLATED_CLOCK = ("ExtrapolatedClock", ExtrapolatedClock)
    HEARTBEAT = ("Heartbeat", Heartbeat)
    LAP_COUNT = ("LapCount", LapCount)
    PIT_LANE_TIME_COLLECTION = ("PitLaneTimeCollection", PitLaneTimeCollection)
    PIT_STOP_SERIES = ("PitStopSeries", PitStopSeries)
    POSITION = ("Position", PositionData)
    RACE_CONTROL_MESSAGES = ("RaceControlMessages", RaceControlMessages)
    SESSION_INFO = ("SessionInfo", SessionInfo)
    TEAM_RADIO = ("TeamRadio", TeamRadio)
    TIMING_APP = ("TimingAppData", TimingApp)
    TIMING_STATS = ("TimingStats", TimingStats)
    TIMING = ("TimingData", Timing)
    TRACK_STATUS = ("TrackStatus", TrackStatus)
    WEATHER = ("WeatherData", Weather)

    def __init__(self, value: str, model: Optional[Type]):
        self._value_ = value
        self._model = model

    @property
    def model(self) -> Optional[Type]:
        """Return the associated model class for this event."""
        return self._model

    @classmethod
    def values(cls) -> list[str]:
        """Return all enum values as a list of strings."""
        return [event.value for event in cls]

    @classmethod
    def from_value(cls, value: str) -> Optional["LiveTimingEvent"]:
        """Return the enum member corresponding to the given value, or None if not found."""
        return next((event for event in cls if event.value == value), None)
