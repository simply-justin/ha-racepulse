from datetime import datetime
from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import Heartbeat

class HeartbeatParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.HEARTBEAT.value

    def parse(self, raw: dict) -> Heartbeat:
        return Heartbeat(timestamp_utc=datetime.fromisoformat(raw["DateTime"].replace("Z", "+00:00")))