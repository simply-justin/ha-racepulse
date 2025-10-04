from ..interfaces import EventParser
from ..models import RawTimingEvent, DriverList, Driver
from ..enums import LiveTimingEvent
from ..decorators import register_parser


@register_parser(LiveTimingEvent.DRIVER_LIST)
class DriverListParser(EventParser):
    """Parse 'DriverList' into DriverList dataclass."""

    def parse(self, raw: "RawTimingEvent") -> DriverList:
        p = raw.payload
        drivers = {}

        for num, d in p.items():
            drivers[num] = Driver(
                racing_number=int(d.get("RacingNumber")),
                broadcast_name=d.get("BroadcastName"),
                full_name=d.get("FullName"),
                tla=d.get("Tla"),
                line=int(d.get("Line")),
                team_name=d.get("TeamName"),
                team_colour=d.get("TeamColour"),
                first_name=d.get("FirstName"),
                last_name=d.get("LastName"),
                reference=d.get("Reference"),
                headshot_url=d.get("HeadshotUrl"),
                public_id_right=d.get("PublicIdRight"),
            )

        return DriverList(drivers=drivers)
