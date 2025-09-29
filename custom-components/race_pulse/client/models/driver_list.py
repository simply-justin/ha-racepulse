from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass(frozen=True)
class DriverInfo:
    """
    Metadata about a Formula 1 driver.

    Attributes:
        racing_number: Driver's official racing number (as string).
        broadcast_name: Short display name for broadcast graphics.
        full_name: Full driver name.
        tla: Three-letter abbreviation (e.g., "NOR").
        line_position: Line number in timing data (updated at end of each lap).
        team_name: Team name (e.g., "McLaren").
        team_color: Hex color string for team branding.
        first_name: Driver's first name.
        last_name: Driver's last name.
        reference: Internal reference code (e.g., "LANNOR01").
        headshot_url: URL to official driver headshot image.
        country_code: ISO country code (e.g., "GBR").
        is_selected: Whether this driver is flagged as selected for display.
    """

    racing_number: Optional[str] = None
    broadcast_name: Optional[str] = None
    full_name: Optional[str] = None
    tla: Optional[str] = None
    line_position: Optional[int] = None
    team_name: Optional[str] = None
    team_color: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    reference: Optional[str] = None
    headshot_url: Optional[str] = None
    country_code: Optional[str] = None
    is_selected: bool = True


@dataclass(frozen=True)
class DriverList:
    """
    A collection of all drivers in the session.

    Attributes:
        drivers: Mapping of driver IDs (usually racing numbers as strings) to driver metadata.
    """

    drivers: Dict[str, DriverInfo] = field(default_factory=dict)
