from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import Position

class PositionParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.POSITION.value

    def map(self, raw: dict) -> Position:
        p = raw["Json"]
        return Position(
