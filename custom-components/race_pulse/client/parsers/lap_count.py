from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import LapCount

class LapCountParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.LAP_COUNT.value

    def parse(self, raw: dict) -> LapCount:
        p = raw["Json"]
        return LapCount(
            current_lap=int(p.get("CurrentLap", 0)),
            total_laps=int(p.get("TotalLaps", 0)),
        )