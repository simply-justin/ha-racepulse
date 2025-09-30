from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class DriverInfo:
    """
    Metadata about a Formula 1 driver.

    Attributes:
        racing_number: Driver's official racing number (as string).
        broadcast_name: Short display name for broadcast graphics.
        full_name: Full driver name.
        tla: Three-letter abbreviation (e.g., "NOR").
        team_name: Team name (e.g., "McLaren").
        team_color: Hex color string for team branding.
        first_name: Driver's first name.
        last_name: Driver's last name.
        reference: Internal reference code (e.g., "LANNOR01").
        headshot_url: URL to official driver headshot image.
        country_code: ISO country code (e.g., "GBR").
        is_selected: Whether this driver is flagged as selected for display.
    """

    racing_number: str = None
    broadcast_name: str = None
    full_name: str = None
    tla: str = None
    team_name: str = None
    team_color: str = None
    first_name: str = None
    last_name: str = None
    reference: str = None
    headshot_url: str = None
    country_code: str = None
    is_selected: bool = True #TODO: check how i want to set the value


@dataclass(frozen=True)
class DriverList:
    """
    A collection of all drivers in the session.

    Attributes:
        drivers: Mapping of driver IDs (usually racing numbers as strings) to driver metadata.
    """

    drivers: Dict[str, DriverInfo]
/// <summary>
/// Sample:
/// <c>
/// "4": {
///   "RacingNumber": "4",
///   "BroadcastName": "L NORRIS",
///   "FullName": "Lando NORRIS",
///   "Tla": "NOR",
///   "Line": 2,
///   "TeamName": "McLaren",
///   "TeamColour": "F58020",
///   "FirstName": "Lando",
///   "LastName": "Norris",
///   "Reference": "LANNOR01",
///   "HeadshotUrl": "https://www.formula1.com/content/dam/fom-website/drivers/L/LANNOR01_Lando_Norris/lannor01.png.transform/1col/image.png",
///   "CountryCode": "GBR"
/// }
/// </c>
/// </summary>
public sealed class DriverListDataPoint
    : Dictionary<string, DriverListDataPoint.Driver>,
        ILiveTimingDataPoint
{
    /// <inheritdoc />
    public LiveTimingDataType LiveTimingDataType => LiveTimingDataType.DriverList;

    public sealed record Driver
    {
        public string? RacingNumber { get; set; }
        public string? BroadcastName { get; set; }
        public string? FullName { get; set; }
        public string? Tla { get; set; }

        /// <summary>
        /// The same as the driver position in <see cref="TimingDataPoint.Driver.Line" />,
        /// however unlike that property this only gets updated at the end of every lap.
        /// </summary>
        public int? Line { get; set; }

        public string? TeamName { get; set; }
        public string? TeamColour { get; set; }

        /// <summary>
        /// Internal property which identifiers whether this driver is "selected" or not.
        /// Unselected drivers are hidden in some displays.
        /// </summary>
        public bool IsSelected { get; set; } = true;
    }
}