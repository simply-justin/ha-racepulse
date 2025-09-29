from datetime import timedelta
from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import ExtrapolatedClock

class ExtrapolatedClockParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.EXTRAPOLATED_CLOCK.value

    def parse(self, raw: dict) -> ExtrapolatedClock:
        p = raw["Json"]
        return ExtrapolatedClock(
            elapsed_time=timedelta(seconds=float(p.get("Elapsed", 0))),
            remaining_time=timedelta(seconds=float(p.get("Remaining", 0))),
            is_extrapolating=bool(p.get("Extrapolating", False)),
        )