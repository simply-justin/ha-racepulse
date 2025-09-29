from datetime import datetime
from ..enums.live_timing_event import LiveTimingEvent
from ..interfaces import EventParser
from ..models import TeamRadio, TeamRadioCapture


class TeamRadioParser(EventParser):
    def supports(self, event_type: str) -> bool:
        return event_type == LiveTimingEvent.TEAM_RADIO.value

    def parse(self, raw: dict) -> TeamRadio:
        captures = []
        for c in raw["Json"].get("Captures", []):
            captures.append(
                TeamRadioCapture(
                    timestamp_utc=datetime.fromisoformat(c["Utc"]),
                    racing_number=c.get("RacingNumber"),
                    file_path=c.get("Path"),
                    download_path=c.get("DownloadFilePath"),
                    transcription=c.get("Transcription"),
                )
            )
        return TeamRadio(captures=captures)
