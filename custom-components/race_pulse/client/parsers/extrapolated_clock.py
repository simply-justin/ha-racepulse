from datetime import timedelta
from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.extrapolated_clock import ExtrapolatedClock
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.EXTRAPOLATED_CLOCK.value)
class ExtrapolatedClockParser(EventParser):
    """Parse 'ExtrapolatedClock' into ExtrapolatedClock dataclass."""

    def parse(self, raw: Dict[str, Any]) -> ExtrapolatedClock:
        p = raw.get("Json", {})
        return ExtrapolatedClock(
            elapsed_time=timedelta(seconds=float(p.get("Utc", 0))),
            remaining_time=timedelta(seconds=float(p.get("Remaining", 0))),
            is_extrapolating=bool(p.get("Extrapolating", False)),
        )
