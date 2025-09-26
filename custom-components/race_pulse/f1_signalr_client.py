import asyncio
import datetime as dt
import logging
from typing import List, Optional

from aiohttp import ClientSession, ClientWebSocketResponse
from homeassistant.core import HomeAssistant
from .interfaces import Notifiable, Observable

_LOGGER = logging.getLogger(__name__)

SUBSCRIBE_MSG = {
    "H": "Streaming",
    "M": "Subscribe",
    "A": [
        [
            "RaceControlMessages",
            "TrackStatus",
            "SessionStatus",
            "WeatherData",
            "LapCount",
        ]
    ],
    "I": 1,
}


class F1SignalRClient(Notifiable):
    """
    SignalR Client for retrieving Formula 1 telemetry data.

    Implements the Notifiable interface to allow Observers to subscribe
    for telemetry updates.
    """

    CONNECTION_URL = "wss://livetiming.formula1.com/signalr/connect"
    NEGOTIATION_URL = "https://livetiming.formula1.com/signalr/negotiate"

    FAST_RETRY_SEC = 5
    MAX_RETRY_SEC = 60
    BACK_OFF_FACTOR = 2

    def __init__(
        self,
        hass: HomeAssistant,
        session: ClientSession,
        observers: Optional[List[Observable]] = None,
    ):
        self._hass = hass
        self._session = session
        self._observers: List[Observable] = observers or []
        self._ws: Optional[ClientWebSocketResponse] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._reconnect_task: Optional[asyncio.Task] = None
        self._t0: Optional[dt.datetime] = None
        self._startup_cutoff: Optional[dt.datetime] = None

    @property
    def connected(self) -> bool:
        """Return True if currently connected to the SignalR hub."""
        return self._ws is not None and not self._ws.closed

    def attach(self, observer: Observable) -> None:
        """Register an observer to receive telemetry updates."""
        if observer not in self._observers:
            self._observers.append(observer)
            _LOGGER.debug("Observer %s attached", observer)

    def detach(self, observer: Observable) -> None:
        """Unregister an observer so it no longer receives telemetry updates."""
        try:
            self._observers.remove(observer)
            _LOGGER.debug("Observer %s detached", observer)
        except ValueError:
            _LOGGER.debug("Attempted to detach unknown observer %s", observer)

    def notify(self, message: any) -> None:
        """Notify all registered observers about a telemetry update."""
        _LOGGER.debug(
            "Notifying %d observers with message: %s", len(self._observers), message
        )
        for observer in self._observers:
            try:
                observer.update(self, message)
            except Exception:
                _LOGGER.exception("Failed to notify observer %s", observer)

    async def connect(self) -> None:
        """
        Establish the SignalR connection with retries and start listening for telemetry.
        Uses exponential backoff if initial connection attempts fail.
        """

        from .const import (
            FAST_RETRY_SEC,
            MAX_RETRY_SEC,
            BACK_OFF_FACTOR,
            HUB_DATA,
            SUBSCRIBE_MSG,
        )

        delay = FAST_RETRY_SEC
        while True:
            try:
                _LOGGER.debug("Starting negotiation with %s", self.NEGOTIATION_URL)

                async with self._session.get(self.NEGOTIATION_URL) as response:
                    response.raise_for_status()
                    data = await response.json()
                    token = data.get("ConnectionToken")
                    cookie = response.headers.get("Set-Cookie")

                if not token:
                    raise RuntimeError(
                        "Negotiation failed: no ConnectionToken received"
                    )

                headers = {
                    "User-Agent": "BestHTTP",
                    "Accept-Encoding": "gzip,identity",
                }
                if cookie:
                    headers["Cookie"] = cookie
                    _LOGGER.debug("Negotiation cookie set")

                params = {
                    "transport": "webSockets",
                    "clientProtocol": "1.5",
                    "connectionToken": token,
                    "connectionData": HUB_DATA,
                }

                _LOGGER.info("Connecting to SignalR hub at %s", self.CONNECTION_URL)
                self._ws = await self._session.ws_connect(
                    self.CONNECTION_URL, params=params, headers=headers
                )

                _LOGGER.debug(
                    "WebSocket connection established, sending subscription message"
                )
                await self._ws.send_json(SUBSCRIBE_MSG)

                # Start heartbeat monitoring
                if self._heartbeat_task is None or self._heartbeat_task.done():
                    self._heartbeat_task = asyncio.create_task(self._heartbeat())
                    _LOGGER.debug("Heartbeat task started")

                self._t0 = dt.datetime.now(dt.timezone.utc)
                self._startup_cutoff = self._t0 - dt.timedelta(seconds=30)
                _LOGGER.info("SignalR connection established successfully")
                return

            except Exception as err:
                _LOGGER.warning(
                    "SignalR connection failed (%s). Retrying in %s seconds …",
                    err,
                    delay,
                )
                await asyncio.sleep(delay)
                delay = min(delay * BACK_OFF_FACTOR, MAX_RETRY_SEC)

    async def disconnect(self) -> None:
        """Gracefully disconnect from the SignalR hub and stop background tasks."""
        _LOGGER.info("Disconnecting from SignalR hub")

        if self._heartbeat_task:
            self._heartbeat_task.cancel()
            self._heartbeat_task = None
            _LOGGER.debug("Heartbeat task cancelled")

        if self._ws is not None:
            await self._ws.close()
            self._ws = None
            _LOGGER.debug("WebSocket connection closed")

    async def _heartbeat(self) -> None:
        """Send periodic heartbeats to keep the connection alive."""
        try:
            while True:
                await asyncio.sleep(300)  # 5 min
                if self._ws is None or self._ws.closed:
                    _LOGGER.debug("Heartbeat stopped: websocket not open")
                    break
                try:
                    await self._ws.send_json(SUBSCRIBE_MSG)
                    _LOGGER.debug("Heartbeat: subscriptions renewed")
                except Exception as exc:
                    _LOGGER.warning("Heartbeat failed: %s", exc)
                    break
        except asyncio.CancelledError:
            _LOGGER.debug("Heartbeat task cancelled by disconnect")
