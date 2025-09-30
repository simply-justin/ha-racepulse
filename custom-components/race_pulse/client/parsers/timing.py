from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.timing import Timing, DriverTiming
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.TIMING.value)
class TimingParser(EventParser):
    """Parse 'TimingData' into Timing with per-driver timing info."""

    def parse(self, raw: Dict[str, Any]) -> Timing:
        p = raw.get("Json", {})
        drivers = {}
        for num, line in p.get("Lines", {}).items():
            drivers[num] = DriverTiming(
                position=line.get("Position"),
                gap_to_leader=line.get("GapToLeader"),
                last_lap_time=line.get("LastLapTime"),
            )
        return Timing(drivers=drivers)


s
