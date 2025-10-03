from dataclasses import dataclass
from typing import Dict
from ..enums import LiveTimingEvent


@dataclass(frozen=True)
class Driver:
    """
    Metadata about a Formula 1 driver.

    Raw example:
        {
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
            "HeadshotUrl": "https: //media.formula1.com/d_driver_fallback_image.png/content/dam/fom-website/drivers/M/MAXVER01_Max_Verstappen/maxver01.png.transform/1col/image.png",
            "PublicIdRight": "common/f1/2025/redbullracing/maxver01/2025redbullracingmaxver01right"
        }
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


@dataclass(frozen=True)
class DriverList:
    """
    A collection of all drivers in the session.

    Source: SignalR event "WeatherData"
    Raw example:
        {
            Drivers: {
                ...
            },
            "_kf": true
        }
    """

    data_type: LiveTimingEvent = LiveTimingEvent.DRIVER_LIST
    drivers: Dict[str, Driver]
