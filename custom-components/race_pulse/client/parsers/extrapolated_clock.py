from datetime import datetime, timedelta
from ..interfaces import EventParser
from ..models import RawTimingEvent, ExtrapolatedClock
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.EXTRAPOLATED_CLOCK)
class ExtrapolatedClockParser(EventParser):
    """Parse 'ExtrapolatedClock' into ExtrapolatedClock dataclass."""

    def parse(self, raw: "RawTimingEvent") -> ExtrapolatedClock:
        p = raw.payload
        return ExtrapolatedClock(
            datetime_utc=datetime.fromisoformat(p.get["Utc"]),
            remaining_time=datetime.strptime(p.get("Remaining", "00:00:00"), "%H:%M:%S").time(),
            extrapolating=bool(p.get("Extrapolating", False))
        )
