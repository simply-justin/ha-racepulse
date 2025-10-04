from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class Segment:
    """ "
    Sector timing information for a driver.

    Raw example:
        {
            "Status": 2048
        }
    """

    status: int


@dataclass(frozen=True)
class Sector:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "Stopped": false,
            "Value": "62.836",
            "Status": 0,
            "OverallFastest": false,
            "PersonalFastest": false,
            "Segments": [
                ...
            ],
            "PreviousValue": "62.836"
        }
    """

    stopped: bool
    value: str
    status: int
    overall_fastest: bool
    personal_fastest: bool
    segments: List[Segment]
    previous_value: Optional[str]


@dataclass(frozen=True)
class SpeedData:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "Value": "179",
            "Status": 0,
            "OverallFastest": false,
            "PersonalFastest": false
        }
    """

    value: int
    status: int
    overall_fastest: bool
    personal_fastest: bool


@dataclass(frozen=True)
class Speed:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "I1": {
                "Value": "253",
                "Status": 0,
                "OverallFastest": false,
                "PersonalFastest": false
            },
            "I2": {
                "Value": "181",
                "Status": 0,
                "OverallFastest": false,
                "PersonalFastest": false
            },
            "FL": {
                "Value": "",
                "Status": 0,
                "OverallFastest": false,
                "PersonalFastest": false
            },
            "ST": {
                "Value": "179",
                "Status": 0,
                "OverallFastest": false,
                "PersonalFastest": false
            }
        }
    """

    i1: SpeedData
    i2: SpeedData
    fl: SpeedData
    st: SpeedData


@dataclass(frozen=True)
class BestLapTime:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "Value": "1:30.857",
            "Lap": 12
        }
    """

    value: str
    lap: int


@dataclass(frozen=True)
class LastLapTime:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "Value": "2:31.237",
            "Status": 0,
            "OverallFastest": false,
            "PersonalFastest": false
        }
    """

    value: str
    status: int
    overall_fastest: bool
    personal_fastest: bool


@dataclass(frozen=True)
class DriverTiming:
    """
    Sector timing information for a driver.

    Raw example:
        "1": {
            "TimeDiffToFastest": "+0.143",
            "TimeDiffToPositionAhead": "+0.011",
            "Line": 3,
            "Position": "3",
            "ShowPosition": true,
            "RacingNumber": "1",
            "Retired": false,
            "InPit": true,
            "PitOut": false,
            "Stopped": false,
            "Status": 1104,
            "Sectors": [
                ...
            ],
            "Speeds": {
                ...
            },
            "BestLapTime": {
                ...
            },
            "LastLapTime": {
                ...
            },
            "NumberOfLaps": 19,
            "NumberOfPitStops": 2
        }
    """

    time_diff_to_fastest: str
    time_diff_to_position_ahead: str
    line: int
    position: str
    show_position: bool
    racing_number: int
    retired: bool
    in_pit: bool
    pit_out: bool
    stopped: bool
    status: int
    sectors: List[Sector]
    speeds: Optional[Speed]
    best_lap_time: Optional[BestLapTime]
    last_lap_time: Optional[LastLapTime]
    number_of_laps: int
    number_of_pit_stops: int


@register_event(LiveTimingEvent.TIMING_DATA)
@dataclass(frozen=True)
class TimingData(Event):
    """
    Full live timing dataset.

    Source: SignalR event "TimingData"
    Raw example:
        {
            "Lines": {
                ...
            },
            "Withheld": False,
            "_kf": True
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.TIMING_DATA
    lines: Dict[str, DriverTiming]
    withheld: bool
