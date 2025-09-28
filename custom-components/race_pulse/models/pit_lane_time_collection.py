from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ..enums.live_timing_event import LiveTimingEvent


@dataclass
class PitLaneTime:
    """
    A single pit lane time entry.

    Attributes:
        duration: Duration spent in the pit lane (string, e.g., "25.4s").
        lap: Lap number when the pit lane entry occurred.
    """
    duration: Optional[str] = None
    lap: Optional[str] = None


@dataclass
class PitLaneTimeCollection:
    """
    Collection of pit lane times for all drivers.

    Attributes:
        data_type: Always set to `LiveTimingEvent.PitLaneTimeCollection`.
        pit_times: Mapping of driver numbers to their most recent pit lane time.
        pit_times_list: Mapping of driver numbers to a list of pit lane time entries.
    """
    data_type: LiveTimingEvent = LiveTimingEvent.PitLaneTimeCollection
    pit_times: Dict[str, PitLaneTime] = field(default_factory=dict)
    pit_times_list: Dict[str, List[PitLaneTime]] = field(default_factory=dict)
