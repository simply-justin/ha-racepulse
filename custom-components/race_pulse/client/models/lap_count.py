from dataclasses import dataclass


@dataclass(frozen=True)
class LapCount:
    """
    Lap count information for a session.

    Attributes:
        data_type: Always set to `LiveTimingEvent.LapCount`.
        current_lap: Current lap number in the session.
        total_laps: Total scheduled laps for the session.
    """

    current_lap: int = 0
    total_laps: int = 0

    def laps_remaining(self) -> int:
        """Return the number of laps remaining in the session."""
        return self.total_laps - self.current_lap
