from ..interfaces import EventParser
from ..models import RawTimingEvent, DriverList, Driver
from ..enums import LiveTimingEvent
from ..decorators import register_parser
from ...helpers import parse_int


@register_parser(LiveTimingEvent.DRIVER_LIST)
class DriverListParser(EventParser[DriverList]):
    """
    Parses a raw 'DriverList' event payload into a structured `DriverList` dataclass.

    This parser converts the raw JSON driver metadata into strongly typed `Driver`
    objects and maps them by their racing number (as a string key).

    Example raw payload structure:
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
                "HeadshotUrl": "https://media.formula1.com/...",
                "PublicIdRight": "common/f1/2025/redbullracing/maxver01/..."
            },
            ...
        }

    Returns:
        A `DriverList` instance containing a mapping of driver IDs to `Driver` objects.
    """

    def parse(self, raw: RawTimingEvent) -> DriverList:
        payload = raw.payload
        drivers: dict[str, Driver] = {}

        for num, data in payload.items():
            drivers[num] = Driver(
                racing_number=parse_int(data["RacingNumber"]),
                broadcast_name=data["BroadcastName"],
                full_name=data["FullName"],
                tla=data["Tla"],
                line=parse_int(data["Line"]),
                team_name=data["TeamName"],
                team_colour=data["TeamColour"],
                first_name=data["FirstName"],
                last_name=data["LastName"],
                reference=data["Reference"],
                headshot_url=data["HeadshotUrl"],
                public_id_right=data["PublicIdRight"],
            )

        return DriverList(drivers=drivers)
