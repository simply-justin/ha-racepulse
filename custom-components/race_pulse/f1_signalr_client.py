import asyncio
import logging
import random
from typing import List, Optional, Any

from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType
from homeassistant.core import HomeAssistant
from .interfaces import Notifiable, Observable

_LOGGER = logging.getLogger(__name__)

CONNECTION_URL = "wss://livetiming.formula1.com/signalr/connect"
NEGOTIATION_URL = "https://livetiming.formula1.com/signalr/negotiate"
HUB_DATA = '[{"name":"Streaming"}]'
SUBSCRIBE_MSG = {
    "H": "Streaming",
    "M": "Subscribe",
    "A": [["RaceControlMessages", "TrackStatus", "SessionStatus", "WeatherData", "LapCount"]],
    "I": 1,
}


class F1SignalRClient(Notifiable):
    """
    SignalR client for receiving Formula 1 live telemetry.

    Features:
    - Handles negotiation and authentication with Formula 1 SignalR API
    - Maintains a persistent WebSocket connection
    - Implements exponential backoff with jitter for reconnection
    - Sends periodic heartbeat pings
    - Forwards all received messages to attached observers
    - Supports multiple observers (attach/detach)

    Usage:
        client = F1SignalRClient(hass, session)
        await client.connect()
        client.attach(observer)
    """

    RETRY_SEC = 5
    MAX_RETRY_SEC = 60
    BACKOFF = 2
    HEARTBEAT = 300

    def __init__(self, hass: HomeAssistant, session: ClientSession):
        self._hass = hass
        self._session = session
        self._observers: List[Observable] = []
        self._ws: Optional[ClientWebSocketResponse] = None
        self._tasks: list[asyncio.Task] = []

    @property
    def connected(self) -> bool:
        return self._ws is not None and not self._ws.closed

    # ---------------- Observer pattern ----------------
    def attach(self, observer: Observable) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            _LOGGER.debug("Observer %s attached", observer)

    def detach(self, observer: Observable) -> None:
        try:
            self._observers.remove(observer)
            _LOGGER.debug("Observer %s detached", observer)
        except ValueError:
            _LOGGER.debug("Attempted to detach unknown observer %s", observer)

    def notify(self, message: Any) -> None:
        for observer in self._observers:
            try:
                observer.update(self, message)
            except Exception:
                _LOGGER.exception("Failed to notify observer %s", observer)

    # ---------------- Connection ----------------
    async def connect(self) -> None:
        """Negotiate and establish WebSocket connection with retries."""
        delay = self.FAST_RETRY_SEC
        while True:
            try:
                _LOGGER.debug("Negotiating connection at %s", self.NEGOTIATION_URL)
                async with self._session.get(self.NEGOTIATION_URL, params={"clientProtocol": "1.5", "connectionData": HUB_DATA}) as response:
                    response.raise_for_status()
                    data = await response.json()
                    token = data.get("ConnectionToken")
                    cookie = response.headers.get("Set-Cookie")

                if not token:
                    raise RuntimeError("Negotiation failed: no ConnectionToken received")

                headers = {"User-Agent": "BestHTTP", "Accept-Encoding": "gzip,identity"}
                if cookie:
                    headers["Cookie"] = cookie

                params = {
                    "transport": "webSockets",
                    "clientProtocol": "1.5",
                    "connectionToken": token,
                    "connectionData": HUB_DATA,
                }

                self._ws = await self._session.ws_connect(self.CONNECTION_URL, params=params, headers=headers)
                await self._ws.send_json(SUBSCRIBE_MSG)

                # background tasks
                self._tasks = [
                    asyncio.create_task(self._heartbeat()),
                    asyncio.create_task(self._listen())
                ]
                _LOGGER.info("SignalR connection established")
                return

            except Exception as err:
                _LOGGER.warning("SignalR connection failed (%s). Retrying in %s sec …", err, delay)
                await asyncio.sleep(delay)
                delay = min(delay * self.BACKOFF, self.MAX_RETRY_SEC) + random.random()

    async def disconnect(self) -> None:
        """Close WebSocket and cancel tasks."""
        for t in self._tasks:
            t.cancel()
        self._tasks.clear()

        if self._ws:
            await self._ws.close()
            self._ws = None

    # ---------------- Tasks ----------------
    async def _heartbeat(self) -> None:
        try:
            while self.connected:
                await asyncio.sleep(self.HEARTBEAT)
                await self._ws.send_json(SUBSCRIBE_MSG)
        except asyncio.CancelledError:
            pass
        except Exception as exc:
            _LOGGER.warning("Heartbeat failed: %s", exc)

    async def _listen(self) -> None:
        try:
            async for msg in self._ws:
                if msg.type == WSMsgType.TEXT:
                    self.notify(msg.json())
                elif msg.type == WSMsgType.ERROR:
                    _LOGGER.error("WebSocket error: %s", msg.data)
                    break
        except asyncio.CancelledError:
            pass
