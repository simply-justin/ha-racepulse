from datetime import datetime
from typing import Dict, Any
from ..interfaces import EventParser, register_parser
from ..models.team_radio import TeamRadio, TeamRadioCapture
from ..enums import LiveTimingEvent


@register_parser(LiveTimingEvent.TEAM_RADIO.value)
class TeamRadioParser(EventParser):
    """Parse 'TeamRadio' into TeamRadio with a list of captures."""

    def parse(self, raw: Dict[str, Any]) -> TeamRadio:
        p = raw.get("Json", {})
        captures = [
            TeamRadioCapture(
                timestamp_utc=datetime.fromisoformat(c["Utc"]),
                racing_number=c.get("RacingNumber"),
                file_path=c.get("Path"),
                download_path=c.get("DownloadFilePath"),
                transcription=c.get("Transcription"),
            )
            for c in p.get("Captures", [])
        ]
        return TeamRadio(captures=captures)
