from ..interfaces import EventParser
from ..models import RawTimingEvent, Heartbeat
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_datetime


@register_parser(LiveTimingEvent.HEARTBEAT)
class HeartbeatParser(EventParser[Heartbeat]):
    """Parses 'Heartbeat' events into a `Heartbeat` dataclass."""

    def parse(self, raw: RawTimingEvent) -> Heartbeat:
        payload = raw.payload

        return Heartbeat(
            datetime_utc=parse_datetime((payload.get("Utc").replace("Z", "+00:00")))
        )
