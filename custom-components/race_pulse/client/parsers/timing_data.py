from ..interfaces import EventParser
from ..models import RawTimingEvent, TimingData, DriverTiming, LastLapTime, BestLapTime, Speed, SpeedData, Sector, Segment
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.TIMING)
class TimingDataParser(EventParser):
    """Parse 'TimingData' into Timing with per-driver timing info."""

    def parse(self, raw: "RawTimingEvent") -> TimingData:
        p = raw.payload
        drivers = {}
        for num, line in p.get("Lines", {}).items():
            drivers[num] = DriverTiming(
                position=line.get("Position"),
                gap_to_leader=line.get("GapToLeader"),
                last_lap_time=line.get("LastLapTime"),
            )
        return TimingData(drivers=drivers)
