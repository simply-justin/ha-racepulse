from ..interfaces import EventParser
from ..models import RawTimingEvent, ExtrapolatedClock
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_bool, parse_datetime, parse_timedelta


@register_parser(LiveTimingEvent.EXTRAPOLATED_CLOCK)
class ExtrapolatedClockParser(EventParser):
    """Parses 'ExtrapolatedClock' payloads into an `ExtrapolatedClock` dataclass."""

    def parse(self, raw: RawTimingEvent) -> ExtrapolatedClock:
        payload = raw.payload

        return ExtrapolatedClock(
            datetime_utc=parse_datetime((payload.get("Utc").replace("Z", "+00:00"))),
            remaining_time=parse_timedelta((payload.get("Remaining", "00:00:00"))),
            extrapolating=parse_bool(payload.get("Extrapolating", False)),
        )
