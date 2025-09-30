from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.timing_app import TimingApp, TimingAppLine
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.TIMING_APP_DATA.value)
class TimingAppParser(EventParser):
    """Parse 'TimingAppData' into TimingApp dataclass."""

    def parse(self, raw: Dict[str, Any]) -> TimingApp:
        p = raw.get("Json", {})
        lines = {
            num: TimingAppLine(
                last_lap_time=line.get("LastLapTime"),
                best_lap_time=line.get("BestLapTime"),
                sector1_time=line.get("S1"),
                sector2_time=line.get("S2"),
                sector3_time=line.get("S3"),
            )
            for num, line in p.get("Lines", {}).items()
        }
        return TimingApp(lines=lines)
