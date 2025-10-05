from dataclasses import dataclass
from typing import Dict, List, Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class Stat:
    """
    Represents a single performance statistic such as a sector or speed value.

    Example of raw JSON payload:
        {
            "Value": "27.019",
            "Position": 6
        }

    Attributes:
        value: The measured value as a string (e.g., "27.019" or "310").
        position: The driver's ranking position for this value (e.g., 1 for fastest).
    """

    value: str
    position: int


@dataclass(frozen=True)
class PersonalBestLapTime(Stat):
    """
    Represents a driver's personal best lap time.

    Example of raw JSON payload:
        {
            "Value": "1:30.857",
            "Lap": 12,
            "Position": 3
        }

    Attributes:
        value: The personal best lap time in "M:SS.mmm" format.
        position: The driver's rank for this lap time (e.g., 1 for fastest overall).
        lap: The lap number on which the personal best was achieved.
    """

    lap: int


@dataclass(frozen=True)
class BestSpeed:
    """
    Represents a driver’s best recorded speeds at key track locations.

    Example of raw JSON payload:
        {
            "I1": { "Value": "310", "Position": 9 },
            "I2": { "Value": "275", "Position": 17 },
            "FL": { "Value": "260", "Position": 4 },
            "ST": { "Value": "301", "Position": 9 }
        }

    Attributes:
        i1: Best speed at the first intermediate point.
        i2: Best speed at the second intermediate point.
        fl: Best speed across the finish line.
        st: Best speed at the speed trap.
    """

    i1: Stat
    i2: Stat
    fl: Stat
    st: Stat


@dataclass(frozen=True)
class DriverStat:
    """
    Represents timing and performance statistics for an individual driver.

    Example of raw JSON payload:
        "1": {
            "Line": 1,
            "RacingNumber": "1",
            "PersonalBestLapTime": {
                "Value": "1:30.857",
                "Lap": 12,
                "Position": 3
            },
            "BestSectors": [
                { "Value": "27.019", "Position": 6 },
                { "Value": "35.487", "Position": 4 },
                { "Value": "28.111", "Position": 3 }
            ],
            "BestSpeeds": {
                "I1": { "Value": "310", "Position": 9 },
                "I2": { "Value": "275", "Position": 17 },
                "FL": { "Value": "260", "Position": 4 },
                "ST": { "Value": "301", "Position": 9 }
            }
        }

    Attributes:
        line: Line index in the timing feed display.
        racing_number: The driver’s car number.
        personal_best_lap_time: The driver’s personal best lap time and ranking.
        best_sectors: List of best sector times (`Stat` instances).
        best_speeds: The driver’s best recorded speeds across track sections.
    """

    line: int
    racing_number: int
    personal_best_lap_time: PersonalBestLapTime
    best_sectors: List[Stat]
    best_speeds: BestSpeed


@register_event(LiveTimingEvent.TIMING_STATS)
@dataclass(frozen=True)
class TimingStats(Event):
    """
    Represents detailed timing statistics for all drivers in a Formula 1 session.

    This event includes personal best laps, sector performances, and best speed
    readings for every driver. It is part of the F1 Live Timing feed and provides
    comparative data between competitors.

    Example of raw event payload:
        {
            "Withheld": false,
            "Lines": {
                "1": { ... },
                "16": { ... }
            },
            "SessionType": "Practice",
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as a `TIMING_STATS` event.
        lines: A mapping of driver identifiers to their corresponding `DriverStat` data.

    Source:
        SignalR event: "TimingStats"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.TIMING_STATS
    lines: Dict[str, DriverStat]
