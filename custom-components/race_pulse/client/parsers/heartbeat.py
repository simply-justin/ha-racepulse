from datetime import datetime
from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.heartbeat import Heartbeat
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.HEARTBEAT.value)
class HeartbeatParser(EventParser):
    """Parse 'Heartbeat' event into Heartbeat dataclass."""

    def parse(self, raw: Dict[str, Any]) -> Heartbeat:
        ts = datetime.fromisoformat(raw["DateTime"].replace("Z", "+00:00"))
        return Heartbeat(timestamp_utc=ts)
