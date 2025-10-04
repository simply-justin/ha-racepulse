from enum import Enum


class LiveTimingEvent(Enum):
    """
    Enumeration of all supported live timing events.
    Each enum value is linked to its corresponding model class.
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
