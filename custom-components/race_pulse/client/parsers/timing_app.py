from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import TimingApp

class TimingAppParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.TIMING_APP.value

    def map(self, raw: dict) -> TimingApp:
        p = raw["Json"]
        return TimingApp(
