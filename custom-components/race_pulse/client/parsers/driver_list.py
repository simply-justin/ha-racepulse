from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import DriverList, DriverInfo


class DriverListParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.DRIVER_LIST.value

    def parse(self, raw: dict) -> DriverList:
        drivers = {}
        for num, data in raw["Json"].items():
            drivers[num] = DriverInfo(
                racing_number=data.get("RacingNumber"),
                broadcast_name=data.get("BroadcastName"),
                full_name=data.get("FullName"),
                tla=data.get("Tla"),
                team_name=data.get("TeamName"),
                team_color=data.get("TeamColour"),
                first_name=data.get("FirstName"),
                last_name=data.get("LastName"),
                reference=data.get("Reference"),
                headshot_url=data.get("HeadshotUrl"),
                country_code=data.get("CountryCode"),
                is_selected=bool(data.get("IsSelected", True)),
            )
        return DriverList(drivers=drivers)
