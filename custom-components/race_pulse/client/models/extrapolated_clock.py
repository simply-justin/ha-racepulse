from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class ExtrapolatedClock:
    """
    Extrapolated session clock.

    Source: SignalR event "ExtrapolatedClock".
    Raw example:
        {
          "Elapsed": "1234.56",
          "Remaining": "245.00",
          "Extrapolating": true
        }

    Attributes:
        elapsed_time: Elapsed session time as timedelta.
        remaining_time: Remaining session time as timedelta.
        is_extrapolating: Whether the system is extrapolating session end.
    """
    elapsed_time: timedelta # Validate if this is current or elapsed
    remaining_time: timedelta
    is_extrapolating: bool
public sealed record ExtrapolatedClockDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.ExtrapolatedClock;

    public DateTimeOffset Utc { get; init; }

    public string Remaining { get; init; } = "99:00:00";

    public bool Extrapolating { get; init; }
}