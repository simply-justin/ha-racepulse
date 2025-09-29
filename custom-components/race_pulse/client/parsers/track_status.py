from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import TrackStatus


class TrackStatusParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.TRACK_STATUS.value

    def parse(self, raw: dict) -> TrackStatus:
        p = raw["Json"]
        return TrackStatus(
            status_flag=p.get("Status", "unknown"),
            message=p.get("Message"),
        )
