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
