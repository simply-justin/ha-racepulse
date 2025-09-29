from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class Interval:
    """
    Gap or interval to another driver.

    Attributes:
        value: String representation of the gap (e.g. "+1.123" or "5L" for 5 laps down).
        catching: Whether the driver is closing the gap.
    """

    value: Optional[str] = None
    catching: Optional[bool] = None


@dataclass(frozen=True)
class Segment:
    """
    Represents a sector segment status.
    Typical values: yellow, green, purple, pit lane, chequered flag.
    """

    status: str


@dataclass(frozen=True)
class SectorTime:
    """
    Timing information for a sector.

    Attributes:
        value: Sector lap time as string.
        is_overall_fastest: True if fastest sector overall.
        is_personal_fastest: True if fastest sector for the driver.
        segments: Mini-sector breakdown with statuses.
    """

    value: Optional[str] = None
    is_overall_fastest: bool = False
    is_personal_fastest: bool = False
    segments: Dict[str, Segment] = field(default_factory=dict)


@dataclass(frozen=True)
class DriverTiming:
    """
    Live timing state for a single driver.

    Attributes:
        gap_to_leader: Gap string (e.g. "LAP 54", "+1.123", "5L").
        interval_to_ahead: Interval to the car ahead.
        racing_line: Driver’s racing line number.
        position: Current position in classification.
        in_pit: Whether the driver is in the pit lane.
        pit_exit: Whether the driver has exited the pits.
        pit_stops: Number of pit stops made.
        is_pit_lap: Whether the current lap is a pit lap.
        completed_laps: Number of laps completed.
        last_lap: Last lap sector times.
        sectors: Per-sector timing for the current lap.
        best_lap_time: Driver’s best lap time.
        knocked_out: Whether eliminated in qualifying.
        retired: Whether retired from session.
        stopped: Whether car is stopped on track.
        status: Current status flag (yellow, pit, chequered, etc.).
    """

    gap_to_leader: Optional[str] = None
    interval_to_ahead: Optional[Interval] = None
    racing_line: Optional[int] = None
    position: Optional[str] = None
    in_pit: bool = False
    pit_exit: bool = False
    pit_stops: int = 0
    is_pit_lap: bool = False
    completed_laps: int = 0
    last_lap: Optional[SectorTime] = None
    sectors: Dict[str, SectorTime] = field(default_factory=dict)
    best_lap_time: Optional[str] = None
    knocked_out: bool = False
    retired: bool = False
    stopped: bool = False
    status: Optional[str] = None


@dataclass(frozen=True)
class Timing:
    """
    Full live timing dataset.

    Attributes:
        drivers: Mapping of driver IDs to their live timing data.
    """

    drivers: Dict[str, DriverTiming] = field(default_factory=dict)
