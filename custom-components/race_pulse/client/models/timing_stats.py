from dataclasses import dataclass
from typing import Dict
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class Stat:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "Value": "27.019",
            "Position": 6
        }
    """

    value: str
    position: int


@dataclass(frozen=True)
class PersonalBestLapTime(Stat):
    """
    Individual timing statistic for a driver.

    Raw example:
        {
            "Value": "1:30.857",
            "Lap": 12,
            "Position": 3
        }
    """

    lap: int


@dataclass(frozen=True)
class BestSpeed:
    """
    Sector timing information for a driver.

    Raw example:
        {
            "I1": {
                "Value": "310",
                "Position": 9
            },
            "I2": {
                "Value": "275",
                "Position": 17
            },
            "FL": {
                "Value": "260",
                "Position": 4
            },
            "ST": {
                "Value": "301",
                "Position": 9
            }
        }
    """

    i1: Stat
    i2: Stat
    fl: Stat
    st: Stat


@dataclass(frozen=True)
class DriverStat:
    """
    Sector timing information for a driver.

    Raw example:
        "1": {
            "Line": 1,
            "RacingNumber": "1",
            "PersonalBestLapTime": {
                ...
            },
            "BestSectors": [
                ...
            ],
            "BestSpeeds": {
                ...
            }
        }
    """

    line: int
    racing_number: int
    personal_best_lap_time: PersonalBestLapTime
    best_sectors: list[Stat]
    best_speeds: BestSpeed


@register_event(LiveTimingEvent.TIMING_STATS)
@dataclass(frozen=True)
class TimingStats(Event):
    """
    Timing statistics for all drivers.
    Source: SignalR event "TimingStats".


    Raw example:
        {
            "Withheld": false,
            "Lines": {
                ...
            },
            "SessionType": "Practice",
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.TIMING_STATS
    lines: Dict[str, DriverStat]
