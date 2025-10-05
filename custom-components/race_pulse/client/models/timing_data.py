from dataclasses import dataclass
from typing import Dict, List, Optional, Final
from ..enums import LiveTimingEvent
from ..interfaces import Event
from ..decorators import register_event


@dataclass(frozen=True)
class Segment:
    """
    Represents an individual micro-sector within a driver's lap sector.

    Example of raw JSON payload:
        {
            "Status": 2048
        }

    Attributes:
        status: The numeric status flag of the segment.
    """

    status: int


@dataclass(frozen=True)
class Sector:
    """
    Represents a single sector's timing information for a driver.

    Example of raw JSON payload:
        {
            "Stopped": false,
            "Value": "62.836",
            "Status": 0,
            "OverallFastest": false,
            "PersonalFastest": false,
            "Segments": [{ "Status": 2048 }],
            "PreviousValue": "62.836"
        }

    Attributes:
        stopped: Whether the driver stopped during this sector.
        value: The recorded sector time as a string (e.g., "62.836").
        status: The numeric status flag for the sector.
        overall_fastest: Whether this sector is the fastest overall.
        personal_fastest: Whether this sector is the driver's personal best.
        segments: A list of micro-segments contained within this sector.
        previous_value: The previous sector time value, if available.
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
    Represents a single speed measurement point within a lap.

    Example of raw JSON payload:
        {
            "Value": "179",
            "Status": 0,
            "OverallFastest": false,
            "PersonalFastest": false
        }

    Attributes:
        value: The recorded speed value (typically in km/h).
        status: The numeric status flag for this speed point.
        overall_fastest: Whether this speed is the fastest overall.
        personal_fastest: Whether this speed is the driver’s personal best.
    """

    value: int
    status: int
    overall_fastest: bool
    personal_fastest: bool


@dataclass(frozen=True)
class Speed:
    """
    Represents a collection of key speed measurements for a driver.

    Example of raw JSON payload:
        {
            "I1": { "Value": "253", "Status": 0, "OverallFastest": false, "PersonalFastest": false },
            "I2": { "Value": "181", "Status": 0, "OverallFastest": false, "PersonalFastest": false },
            "FL": { "Value": "", "Status": 0, "OverallFastest": false, "PersonalFastest": false },
            "ST": { "Value": "179", "Status": 0, "OverallFastest": false, "PersonalFastest": false }
        }

    Attributes:
        i1: Speed at the first intermediate point.
        i2: Speed at the second intermediate point.
        fl: Finish line speed.
        st: Speed trap measurement.
    """

    i1: SpeedData
    i2: SpeedData
    fl: SpeedData
    st: SpeedData


@dataclass(frozen=True)
class BestLapTime:
    """
    Represents a driver's best lap time and the lap number it occurred on.

    Example of raw JSON payload:
        {
            "Value": "1:30.857",
            "Lap": 12
        }

    Attributes:
        value: The best lap time in "M:SS.mmm" format.
        lap: The lap number on which the best time was set.
    """

    value: str
    lap: int


@dataclass(frozen=True)
class LastLapTime:
    """
    Represents a driver's most recently completed lap time.

    Example of raw JSON payload:
        {
            "Value": "2:31.237",
            "Status": 0,
            "OverallFastest": false,
            "PersonalFastest": false
        }

    Attributes:
        value: The lap time as a string (e.g., "2:31.237").
        status: The numeric status flag for the lap.
        overall_fastest: Whether this lap is the fastest overall.
        personal_fastest: Whether this lap is the driver’s personal best.
    """

    value: str
    status: int
    overall_fastest: bool
    personal_fastest: bool


@dataclass(frozen=True)
class DriverTiming:
    """
    Represents full timing data for a single driver, including position, sectors, and lap statistics.

    Example of raw JSON payload:
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
            "Sectors": [ ... ],
            "Speeds": { ... },
            "BestLapTime": { ... },
            "LastLapTime": { ... },
            "NumberOfLaps": 19,
            "NumberOfPitStops": 2
        }

    Attributes:
        time_diff_to_fastest: Time difference to the fastest driver (e.g., "+0.143").
        time_diff_to_position_ahead: Time difference to the driver ahead (e.g., "+0.011").
        line: The driver's line index in the timing display.
        position: The driver's current position as a string.
        show_position: Whether the position should be displayed.
        racing_number: The driver's car number.
        retired: Whether the driver has retired from the session.
        in_pit: Whether the driver is currently in the pit lane.
        pit_out: Whether the driver is exiting the pit lane.
        stopped: Whether the driver has stopped on track.
        status: The numeric driver status flag.
        sectors: List of sector timing data for the current lap.
        speeds: Optional `Speed` data representing key speed trap points.
        best_lap_time: Optional `BestLapTime` data for the driver's best lap.
        last_lap_time: Optional `LastLapTime` data for the most recent lap.
        number_of_laps: Total laps completed by the driver.
        number_of_pit_stops: Number of pit stops made during the session.
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
    Represents the full live timing dataset for all drivers.

    This event contains the most granular level of timing data, including
    per-driver sector times, speeds, lap information, and pit data. It is
    continuously updated during a Formula 1 session.

    Example of raw event payload:
        {
            "Lines": {
                "1": { ... },
                "16": { ... }
            },
            "Withheld": false,
            "_kf": true
        }

    Attributes:
        data_type: A constant identifying this event as a `TIMING_DATA` event.
        lines: A mapping of driver identifiers to their corresponding `DriverTiming` objects.
        withheld: Whether the timing data is currently withheld from the public feed.

    Source:
        SignalR event: "TimingData"
    """

    data_type: Final[LiveTimingEvent] = LiveTimingEvent.TIMING_DATA
    lines: Dict[str, DriverTiming]
    withheld: bool
