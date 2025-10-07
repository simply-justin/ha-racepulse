from dataclasses import dataclass
from typing import Dict
from ..interfaces import Event
from ..enums import LiveTimingEvent
from ..decorators import register_event


@dataclass(frozen=True)
class Driver:
    """
    Represents metadata about a Formula 1 driver as provided by the F1 Live Timing API.

    Each driver entry includes personal details, team information, and associated media identifiers.

    Example of raw API data:
        {
            "1": {
                "RacingNumber": "1",
                "BroadcastName": "M VERSTAPPEN",
                "FullName": "Max VERSTAPPEN",
                "Tla": "VER",
                "Line": 3,
                "TeamName": "Red Bull Racing",
                "TeamColour": "4781D7",
                "FirstName": "Max",
                "LastName": "Verstappen",
                "Reference": "MAXVER01",
                "HeadshotUrl": "https://media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
                "PublicIdRight": "common/f1/2025/redbullracing/maxver01/2025redbullracingmaxver01right"
            }
        }

    Attributes:
        racing_number: The driver's car number as displayed on timing screens.
        broadcast_name: The abbreviated name used in TV and timing overlays.
        full_name: The driver's full name in uppercase format.
        tla: The three-letter abbreviation (TLA) representing the driver.
        line: An integer used for ordering or layout purposes in live timing.
        team_name: The full name of the team the driver belongs to.
        team_colour: The team's color code in hexadecimal format (e.g. "4781D7").
        first_name: The driver's given name.
        last_name: The driver's family name.
        reference: The driver's unique reference identifier used in API data.
        headshot_url: A URL pointing to the driver's headshot image.
        public_id_right: A path reference for media assets related to the driver.
    """

    racing_number: int
    broadcast_name: str
    full_name: str
    tla: str
    line: int
    team_name: str
    team_colour: str
    first_name: str
    last_name: str
    reference: str
    headshot_url: str
    public_id_right: str


@register_event(LiveTimingEvent.DRIVER_LIST.value)
@dataclass(frozen=True)
class DriverList(Event):
    """
    Represents the list of all drivers participating in a Formula 1 session.

    This event is typically emitted by the F1 Live Timing service under the
    `LiveTimingEvent.DRIVER_LIST` event type. It contains metadata for each
    driver, indexed by their racing number or unique ID.

    Example of raw event payload:
        {
            "Drivers": {
                "1": { ... },  # Max Verstappen
                "16": { ... }, # Charles Leclerc
                ...
            },
            "_kf": true
        }

    Attributes:
        data_type: Identifies this event as a `DRIVER_LIST` event.
        drivers: A mapping of driver IDs (as strings) to their corresponding `Driver` objects.

    Source:
        SignalR event: "DriverList"
    """

    data_type: LiveTimingEvent = LiveTimingEvent.DRIVER_LIST
    drivers: Dict[str, "Driver"]
