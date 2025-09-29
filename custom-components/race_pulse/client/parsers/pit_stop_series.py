from datetime import datetime
from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import PitStopSeries, PitStopTime, PitStopEntry


class PitStopSeriesParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.PIT_STOP_SERIES.value

    def parse(self, raw: dict) -> PitStopSeries:
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
