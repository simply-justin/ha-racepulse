from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import PitLaneTimeCollection

class PitLaneTimeCollectionParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.PIT_LANE_TIME_COLLECTION.value

    def map(self, raw: dict) -> PitLaneTimeCollection:
        p = raw["Json"]
        return PitLaneTimeCollection(
