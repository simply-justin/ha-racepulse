from datetime import datetime
from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.race_control_messages import RaceControlMessages, RaceControlMessage
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.RACE_CONTROL_MESSAGES.value)
class RaceControlMessagesParser(EventParser):
    """Parse 'RaceControlMessages' into RaceControlMessages dataclass."""

    def parse(self, raw: Dict[str, Any]) -> RaceControlMessages:
        p = raw.get("Json", {})
        messages = [
            RaceControlMessage(
                timestamp_utc=datetime.fromisoformat(m["Utc"]),
                text=m["Message"],
            )
            for m in p.get("Messages", [])
        ]
        return RaceControlMessages(messages=messages)
aa