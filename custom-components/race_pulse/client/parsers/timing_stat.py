from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import TimingStats, DriverStats, Stat

class TimingStatsParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.TIMING_STATS.value

    def parse(self, raw: dict) -> TimingStats:
        drivers = {}
        for num, line in raw["Json"].get("Lines", {}).items():
            best_speeds = {
                key: Stat(value=stat.get("Value"), position=stat.get("Position"))
                for key, stat in line.get("BestSpeeds", {}).items()
            }
            drivers[num] = DriverStats(best_speeds=best_speeds)
        return TimingStats(drivers=drivers)