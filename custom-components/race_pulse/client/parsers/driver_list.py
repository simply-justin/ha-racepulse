from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.driver_list import DriverList, DriverInfo
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.DRIVER_LIST.value)
class DriverListParser(EventParser):
    """Parse 'DriverList' into DriverList dataclass."""

    def parse(self, raw: Dict[str, Any]) -> DriverList:
        p = raw.get("Json", {})
        drivers = {}
        for num, d in p.items():
            drivers[num] = DriverInfo(
                racing_number=d.get("RacingNumber"),
                broadcast_name=d.get("BroadcastName"),
                full_name=d.get("FullName"),
                tla=d.get("Tla"),
                team_name=d.get("TeamName"),
                team_color=d.get("TeamColour"),
                first_name=d.get("FirstName"),
                last_name=d.get("LastName"),
                reference=d.get("Reference"),
                headshot_url=d.get("HeadshotUrl"),
                country_code=d.get("CountryCode"),
            )
        return DriverList(drivers=drivers)
