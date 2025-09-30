from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.timing_stat import TimingStats, DriverStats, Stat
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.TIMING_STATS.value)
class TimingStatsParser(EventParser):
    """Parse 'TimingStats' into TimingStats dataclass."""

    def parse(self, raw: Dict[str, Any]) -> TimingStats:
        p = raw.get("Json", {})
        drivers = {}
        for num, line in p.get("Lines", {}).items():
            best_speeds = {
                k: Stat(
                    value=float(stat.get("Value", 0.0)),
                    position=int(stat.get("Position", 0)),
                )
                for k, stat in line.get("BestSpeeds", {}).items()
            }
            drivers[num] = DriverStats(best_speeds=best_speeds)
        return TimingStats(drivers=drivers)
