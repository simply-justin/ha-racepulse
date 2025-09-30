from datetime import datetime
from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.pit_stop_series import PitStopSeries, PitStopTime, PitStopEntry
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.PIT_STOP_SERIES.value)
class PitStopSeriesParser(EventParser):
    """Parse 'PitStopSeries' into PitStopSeries dataclass."""

    def parse(self, raw: Dict[str, Any]) -> PitStopSeries:
        pit_times = {}
        for driver, laps in raw["Json"].get("PitTimes", {}).items():
            driver_pits = {}
            for lap, entry in laps.items():
                driver_pits[lap] = PitStopTime(
                    timestamp_utc=datetime.fromisoformat(entry["Utc"]),
                    pit_stop=PitStopEntry(
                        racing_number=entry.get("RacingNumber"),
                        pit_stop_time=entry.get("PitStopTime"),
                        pit_lane_time=entry.get("PitLaneTime"),
                        lap=entry.get("Lap"),
                    ),
                )
            pit_times[driver] = driver_pits
        return PitStopSeries(pit_times=pit_times)
aa