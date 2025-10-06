import json
from pathlib import Path
from homeassistant.const import Platform

manifest_path = Path(__file__).parent / "manifest.json"
with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

NAME = manifest.get('name')
DOMAIN = manifest.get('domain')
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = manifest.get('version')
ISSUE_URL = manifest.get('issue_tracker')

PLATFORMS = [Platform.BINARY_SENSOR, Platform.SENSOR]

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""