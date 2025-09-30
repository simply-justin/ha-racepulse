from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass(frozen=True)
class TeamRadioCapture:
    """
    A single captured piece of team radio.

    Attributes:
        timestamp_utc: UTC timestamp of the radio capture.
        racing_number: Driver’s racing number.
        file_path: Path to the audio file relative to the F1 storage.
        download_path: Local path where the file is stored (if downloaded).
        transcription: Transcribed text of the radio message (if available).
    """

    timestamp_utc: datetime
    racing_number: str
    file_path: Optional[str] = None
    download_path: Optional[str] = None
    transcription: Optional[str] = None


@dataclass(frozen=True)
class TeamRadio:
    """
    Collection of all captured team radio messages for a session.

    Attributes:
        captures: List of captured radio messages.
    """

    captures: List[TeamRadioCapture] = field(default_factory=list)
/// <summary>
/// Sample:
/// <c>
/// {
///    "Captures": [
///      {
///        "Utc": "2024-05-26T12:15:25.71Z",
///        "RacingNumber": "81",
///        "Path": "TeamRadio/OSCPIA01_81_20240525_171518.mp3"
///      },
///      {
///        "Utc": "2024-05-26T12:15:25.8662788Z",
///        "RacingNumber": "4",
///        "Path": "TeamRadio/LANNOR01_4_20240526_141522.mp3"
///      }
///    ]
/// }
/// </c>
/// </summary>
public sealed class TeamRadioDataPoint : ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.TeamRadio;

    public Dictionary<string, Capture> Captures { get; set; } = new();

    public sealed record Capture
    {
        public DateTimeOffset? Utc { get; set; }
        public string? RacingNumber { get; set; }
        public string? Path { get; set; }

        public string? DownloadedFilePath { get; set; }

        /// <summary>
        /// This field is populated by us on-demand and not the Live Timing feed
        /// </summary>
        public string? Transcription { get; set; }
    }
}