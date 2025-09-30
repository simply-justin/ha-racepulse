from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TrackStatus:
    """
    Current track status information.

    Attributes:
        status_flag: Current track flag condition (e.g., "green", "yellow", "red").
        message: Optional descriptive message (e.g., "Yellow in sector 1").
    """

    status_flag: str = "unknown"
    message: Optional[str] = None
/// <summary>
/// Sample: {"Status": "2", "Message": "Yellow", "_kf": true}
/// </summary>
public sealed record TrackStatusDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.TrackStatus;

    public string? Status { get; set; }
    public string? Message { get; set; }
}