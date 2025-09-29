from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import Timing, DriverTiming

class TimingParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.TIMING.value

    def parse(self, raw: dict) -> Timing:
        drivers = {}
        for num, line in raw["Json"].get("Lines", {}).items():
            drivers[num] = DriverTiming(
                position=line.get("Position"),
                gap_to_leader=line.get("GapToLeader"),
                last_lap_time=line.get("LastLapTime"),
            )
        return Timing(drivers=drivers)
    cccc