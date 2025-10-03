from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class PitLaneTime:
    """
    A single pit lane time entry.

    Attributes:
        duration: Duration spent in the pit lane (string, e.g., "25.4s").
        lap: Lap number when the pit lane entry occurred.
    """

    duration: Optional[str] = None
    lap: Optional[str] = None


@dataclass(frozen=True)
class PitLaneTimeCollection:
    """
    Collection of pit lane times for all drivers.

    Source: SignalR event "WeatherData"
    Raw example:
        {
            "AirTemp": "28.5",
            "Humidity": "73.0",
            "Pressure": "1012.6",
            "Rainfall": "0",
            "TrackTemp": "32.5",
            "WindDirection": "115",
            "WindSpeed": "0.5",
            "_kf": true
        }
    """

    pit_times: Dict[str, PitLaneTime] = field(default_factory=dict)
    pit_times_list: Dict[str, List[PitLaneTime]] = field(default_factory=dict)
    data_type: LiveTimingEvent = LiveTimingEvent.TRACK_STATUS
    
    # "PitLaneTimeCollection": {
    #         "PitTimes": {},
    #         "_kf": true
    #     },