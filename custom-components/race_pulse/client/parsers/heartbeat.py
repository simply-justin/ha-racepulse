from datetime import datetime
from ..interfaces import EventParser
from ..models import RawTimingEvent, Heartbeat
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.HEARTBEAT)
class HeartbeatParser(EventParser):
    """Parse 'Heartbeat' event into Heartbeat dataclass."""

    def parse(self, raw: "RawTimingEvent") -> Heartbeat:
        ts = datetime.fromisoformat(raw.payload["Utx"].replace("Z", "+00:00"))
        return Heartbeat(datetime_utc=ts)
