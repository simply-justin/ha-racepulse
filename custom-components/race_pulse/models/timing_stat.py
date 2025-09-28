from dataclasses import dataclass, field
from typing import Dict, Optional
from ..enums.live_timing_event import LiveTimingEvent


@dataclass
class Stat:
    """
    A single statistical value.

    Attributes:
        value: Recorded value (e.g., speed in km/h) as a string.
        position: Ranking position of the driver for this stat.
    """
    value: Optional[str] = None
    position: Optional[int] = None


@dataclass
class DriverStats:
    """
    Statistics for a single driver.

    Attributes:
        best_speeds: Dictionary of stat categories to their values.
                     Example keys: "speed_trap", "sector1", "sector2", "sector3".
    """
    best_speeds: Dict[str, Stat] = field(default_factory=dict)


@dataclass
class TimingStats:
    """
    Timing statistics data point for all drivers.

    Attributes:
        data_type: Always set to `LiveTimingEvent.TimingStats`.
        drivers: Mapping of driver IDs to their statistics.
    """
    data_type: LiveTimingEvent = LiveTimingEvent.TimingStats
    drivers: Dict[str, DriverStats] = field(default_factory=dict)
