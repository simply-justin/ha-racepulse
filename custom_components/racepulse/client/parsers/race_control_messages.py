from ..interfaces import EventParser
from ..models import RawTimingEvent, RaceControlMessages, RaceControlMessage
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int, parse_datetime


@register_parser(LiveTimingEvent.RACE_CONTROL_MESSAGES)
class RaceControlMessagesParser(EventParser[RaceControlMessages]):
    """Parses 'RaceControlMessages' events into a `RaceControlMessages` dataclass."""

    def parse(self, raw: RawTimingEvent) -> RaceControlMessages:
        payload = raw.payload
        messages_data = payload.get("Messages", [])

        messages = []
        for m in messages_data:
            messages.append(
                RaceControlMessage(
                    datetime_utc=parse_datetime((m.get("Utc").replace("Z", "+00:00"))),
                    category=m.get("Category"),
                    flag=m.get("Flag"),
                    scope=m.get("Scope"),
                    sector=parse_int(m.get("Sector")),
                    message=m.get("Message", ""),
                )
            )

        return RaceControlMessages(messages=messages)
