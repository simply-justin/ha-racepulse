from dataclasses import dataclass
from datetime import timedelta
from ..enums.live_timing_event import LiveTimingEvent


@dataclass
class ExtrapolatedClock:
    """
    Extrapolated session clock data.

    Attributes:
        data_type: Always set to `LiveTimingEvent.ExtrapolatedClock`.
        elapsed_time: Extrapolated session elapsed time.
        remaining_time: Extrapolated session remaining time.
        is_extrapolating: Whether extrapolation is currently applied.
    """

    data_type: LiveTimingEvent = LiveTimingEvent.ExtrapolatedClock
    elapsed_time: timedelta = timedelta(0)
    remaining_time: timedelta = timedelta(0)
    is_extrapolating: bool = False