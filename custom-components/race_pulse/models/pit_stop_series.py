from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional
from ..enums.live_timing_event import LiveTimingEvent


@dataclass
class PitStopEntry:
    """
    Details of a single pit stop.

    Attributes:
        racing_number: Driver's racing number.
        pit_stop_time: Duration of the pit stop (string, e.g., "2.5s").
        pit_lane_time: Total time spent in the pit lane (string).
        lap: Lap number when the pit stop occurred.
    """
    racing_number: Optional[str] = None
    pit_stop_time: Optional[str] = None
    pit_lane_time: Optional[str] = None
    lap: Optional[str] = None


@dataclass
class PitStopTime:
    """
    Timestamped record of a pit stop.

    Attributes:
        timestamp_utc: UTC time when the pit stop occurred.
        pit_stop: Pit stop entry details.
    """
    timestamp_utc: Optional[datetime] = None
    pit_stop: Optional[PitStopEntry] = None


@dataclass
class PitStopSeries:
    """
    Series of pit stops for all drivers.

    Attributes:
        data_type: Always set to `LiveTimingEvent.PitStopSeries`.
        pit_times: Nested mapping of driver -> lap -> pit stop time.
    """
    data_type: LiveTimingEvent = LiveTimingEvent.PitStopSeries
    pit_times: Dict[str, Dict[str, PitStopTime]] = field(default_factory=dict)
