import asyncio
import logging
from datetime import timedelta
from typing import TYPE_CHECKING

from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.config_entries import ConfigEntry
from homeassistant.core_config import Config
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, PLATFORMS, STARTUP_MESSAGE
from .client import F1SignalRClient

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

SCAN_INTERVAL = timedelta(seconds=30)
_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up the F1 Live Timing integration from a config entry."""

    session = async_get_clientsession(hass)
    client = F1SignalRClient(session)

    connect_task = hass.async_create_task(client.connect())

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        "connect_task": connect_task,
    }

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    _LOGGER.info("[%s] Integration setup complete", DOMAIN)

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload the F1 Live Timing config entry."""
    data = hass.data[DOMAIN].pop(entry.entry_id, None)

    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])

    if data:
        client: F1SignalRClient = data["client"]
        connect_task = data["connect_task"]

        # Ask client to stop reconnect loop and close WS
        await client.disconnect()

        # Now cancel/await the outer loop task that HA owns
        if not connect_task.done():
            connect_task.cancel()

    _LOGGER.info("[%s] Integration unloaded", DOMAIN)
    return unload_ok


async def async_reload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
