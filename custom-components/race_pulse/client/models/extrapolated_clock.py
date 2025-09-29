from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class ExtrapolatedClock:
    """
    Extrapolated session clock data.

    Attributes:
        elapsed_time: Extrapolated session elapsed time.
        remaining_time: Extrapolated session remaining time.
        is_extrapolating: Whether extrapolation is currently applied.
    """

    elapsed_time: timedelta = timedelta(0)
    remaining_time: timedelta = timedelta(0)
    is_extrapolating: bool = False
