from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class Stint:
    """
    Represents a tyre stint for a driver.

    Attributes:
        lap_flags: Flags for special lap conditions (e.g., pit, SC).
        compound: Tyre compound used (e.g., "SOFT", "MEDIUM", "HARD").
        is_new: Whether the tyres were new at the start of the stint.
        total_laps: Total laps completed on this stint.
        start_laps: Starting lap number for this stint.
        lap_time: Best lap time achieved in this stint (string).
    """

    lap_flags: Optional[int] = None
    compound: Optional[str] = None
    is_new: Optional[bool] = None
    total_laps: Optional[int] = None
    start_laps: Optional[int] = None
    lap_time: Optional[str] = None


@dataclass(frozen=True)
class DriverStints:
    """
    Tyre stint and strategy data for a driver.

    Attributes:
        grid_position: Starting grid position (only in race sessions).
        line_position: Timing line reference.
        stints: Dictionary of stint identifiers to stint details.
    """

    grid_position: Optional[str] = None
    line_position: Optional[int] = None
    stints: Dict[str, Stint] = field(default_factory=dict)


@dataclass(frozen=True)
class TimingApp:
    """
    Strategy and tyre data for all drivers.

    Attributes:
        drivers: Mapping of driver IDs to their stint data.
    """

    drivers: Dict[str, DriverStints] = field(default_factory=dict)
