from datetime import datetime
from ..interfaces import EventParser
from ..models import RawTimingEvent, RaceControlMessages, RaceControlMessage
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.RACE_CONTROL_MESSAGES)
class RaceControlMessagesParser(EventParser):
    """Parse 'RaceControlMessages' into RaceControlMessages dataclass."""

    def parse(self, raw: "RawTimingEvent") -> RaceControlMessages:
        p = raw.payload
        messages = [
            RaceControlMessage(
                datetime_utc=datetime.fromisoformat(m["Utc"]),
                category=m.get("Category", None),
                flag=m.get("Flag", None),
                scope=m.get("Scope", None),
                sector=m.get("Sector", None),
                message=m.get("Message", "")
            )
            for m in p.get("Messages", [])
        ]
        return RaceControlMessages(messages=messages)
