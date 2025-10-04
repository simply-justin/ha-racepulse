from ..interfaces import EventParser
from ..models import RawTimingEvent, TimingApp, DriverStints, Stint
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.TIMING_APP_DATA)
class TimingAppParser(EventParser):
    """Parse 'TimingAppData' into TimingApp dataclass."""

    def parse(self, raw: "RawTimingEvent") -> TimingApp:
        p = raw.payload
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
