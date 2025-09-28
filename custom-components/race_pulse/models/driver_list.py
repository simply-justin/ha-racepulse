from dataclasses import dataclass, field
from typing import Dict, Optional
from ..enums.live_timing_event import LiveTimingEvent


@dataclass
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


@dataclass
class DriverList:
    """
    A collection of all drivers in the session.

    Attributes:
        data_type: Always set to `LiveTimingEvent.DriverList`.
        drivers: Mapping of driver IDs (usually racing numbers as strings) to driver metadata.
    """

    data_type: LiveTimingEvent = LiveTimingEvent.DriverList
    drivers: Dict[str, DriverInfo] = field(default_factory=dict)

#     /// <summary>
# /// Sample:
# /// <c>
# /// "4": {
# ///   "RacingNumber": "4",
# ///   "BroadcastName": "L NORRIS",
# ///   "FullName": "Lando NORRIS",
# ///   "Tla": "NOR",
# ///   "Line": 2,
# ///   "TeamName": "McLaren",
# ///   "TeamColour": "F58020",
# ///   "FirstName": "Lando",
# ///   "LastName": "Norris",
# ///   "Reference": "LANNOR01",
# ///   "HeadshotUrl": "https://www.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/1col/image.png",
# ///   "CountryCode": "GBR"
# /// }
# /// </c>
# /// </summary>
# public sealed class DriverListDataPoint
#     : Dictionary<string, DriverListDataPoint.Driver>,
#         ILiveTimingDataPoint
# {
#     /// <inheritdoc />
#     public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.DriverList;

#     public sealed record Driver
#     {
#         public string? RacingNumber { get; set; }
#         public string? BroadcastName { get; set; }
#         public string? FullName { get; set; }
#         public string? Tla { get; set; }

#         /// <summary>
#         /// The same as the driver position in <see cref="TimingDataPoint.Driver.Line" />,
#         /// however unlike that property this only gets updated at the end of every lap.
#         /// </summary>
#         public int? Line { get; set; }

#         public string? TeamName { get; set; }
#         public string? TeamColour { get; set; }

#         /// <summary>
#         /// Internal property which identifiers whether this driver is "selected" or not.
#         /// Unselected drivers are hidden in some displays.
#         /// </summary>
#         public bool IsSelected { get; set; } = true;
#     }
# }