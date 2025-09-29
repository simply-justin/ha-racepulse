from dataclasses import dataclass, field
from datetime import datetime
from typing import List

@dataclass(frozen=True)
class RaceControlMessage:
    """
    A single race control message issued by the FIA.

    Attributes:
        timestamp_utc: UTC timestamp when the message was issued.
        text: Human-readable message (e.g., "GREEN LIGHT - PIT EXIT OPEN").
    """
    timestamp_utc: datetime
    text: str


@dataclass(frozen=True)
class RaceControlMessages:
    """
    Collection of race control messages during a session.

    Attributes:
        messages: List of race control messages in chronological order.
    """
    messages: List[RaceControlMessage] = field(default_factory=list)
