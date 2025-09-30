from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.pit_lane_time_collection import PitLaneTimeCollection, PitLaneTime
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.PIT_LANE_TIME_COLLECTION.value)
class PitLaneTimeCollectionParser(EventParser):
    """Parse 'PitLaneTimeCollection' into PitLaneTimeCollection dataclass."""

    def parse(self, raw: Dict[str, Any]) -> PitLaneTimeCollection:
        pit_times = {
            driver: PitLaneTime(duration=e.get("Duration"), lap=e.get("Lap"))
            for driver, e in raw["Json"].get("PitTimes", {}).items()
        }
        pit_times_list = {
            driver: [
                PitLaneTime(duration=x.get("Duration"), lap=x.get("Lap"))
                for x in entries
            ]
            for driver, entries in raw["Json"].get("PitTimesList", {}).items()
        }
        return PitLaneTimeCollection(pit_times=pit_times, pit_times_list=pit_times_list)
aa