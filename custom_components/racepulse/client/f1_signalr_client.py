import asyncio
from aiohttp import WSMsgType
import json
import logging
from typing import TYPE_CHECKING, Optional, Tuple

from .enums.live_timing_event import LiveTimingEvent
from .interfaces.event import Event
from .interfaces.notifiable import Notifiable
from .interfaces.observable import Observable
from .event_factory import EventFactory
from .decorators import _EVENT_REGISTRY
from ..const import DOMAIN


if TYPE_CHECKING:
    from aiohttp import ClientSession, ClientWebSocketResponse

_LOGGER = logging.getLogger(__name__)

HUB_DATA = '[{"name":"Streaming"}]'
SUBSCRIBE_MSG = {
    "H": "Streaming",
    "M": "Subscribe",
    "A": [list(_EVENT_REGISTRY.keys())],
    "I": 1,
}

# TODO: Implement Paid Logic. (Getting credentials from HA)


class F1SignalRClient(Notifiable):
    """
    Asynchronous client for connecting to the Formula 1 live timing SignalR service.
    """

    NEGOTIATION_URL = "https://livetiming.formula1.com/signalr/negotiate"
    CONNECTION_URL = "wss://livetiming.formula1.com/signalr/connect"

    HEARTBEAT = 300  # Seconds between keep-alive messages
    FAST_RETRY_SEC = 5
    MAX_RETRY_SEC = 60
    BACK_OFF = 2  # Exponential backoff multiplier

    def __init__(self, session: "ClientSession"):
        self._session = session
        self._observers: list[Observable] = []
        self._ws: Optional["ClientWebSocketResponse"] = None
        self._tasks: list[asyncio.Task] = []
        self._reconnect: bool = True

    @property
    def connected(self) -> bool:
        """Whether the websocket is currently connected."""
        return self._ws is not None and not self._ws.closed

    # ---------------- Observer pattern ----------------
    def attach(self, observer: Observable) -> None:
        """Attach an observer that will receive event notifications."""
        if observer not in self._observers:
            self._observers.append(observer)
            _LOGGER.debug("[%s] Attached observer: %s", DOMAIN, observer)

    def detach(self, observer: Observable) -> None:
        """Detach a previously attached observer."""
        if observer in self._observers:
            self._observers.remove(observer)
            _LOGGER.debug("[%s] Detached observer: %s", DOMAIN, observer)

    def notify(self, message: Event) -> None:
        """Notify all observers about a new event."""
        for observer in self._observers:
            try:
                observer.update(self, message)
            except Exception:
                _LOGGER.exception("[%s] Failed to notify observer: %s", DOMAIN, observer)

    # ---------------- Connection Lifecycle ----------------
    async def connect(self) -> None:
        """
        Establish and maintain a persistent connection to the F1 SignalR endpoint.

        Implements automatic retry with exponential backoff.
        """
        delay = self.FAST_RETRY_SEC
        attempt = 0

        while self._reconnect:
            attempt += 1
            try:
                # Token negotiation.
                token, cookie = await self._negotiate()
                if not token:
                    raise RuntimeError("Negotiation failed — missing connection token")

                headers = {"User-Agent": "BestHTTP", "Accept-Encoding": "gzip,identity"}
                if cookie:
                    headers["Cookie"] = cookie

                # Open a new connection to the F1 socket.
                self._ws = await self._session.ws_connect(
                    self.CONNECTION_URL,
                    params={
                        "transport": "webSockets",
                        "clientProtocol": "1.5",
                        "connectionToken": token,
                        "connectionData": HUB_DATA,
                    },
                    headers=headers,
                )

                # Subscribe to the events defined in the EVENT_REGISTRY.
                await self._ws.send_json(SUBSCRIBE_MSG)
                _LOGGER.info("[%s] Connected to F1 live timing stream", DOMAIN)

                # Reset backoff after successful connection
                delay = self.FAST_RETRY_SEC

                # Wait for either task to finish (e.g., socket closes)
                done, _ = await asyncio.wait(
                    self._tasks, return_when=asyncio.FIRST_COMPLETED
                )

                # Handle task exceptions
                for t in done:
                    if not t.cancelled() and (exc := t.exception()):
                        _LOGGER.error("[%s] Task error: %s", DOMAIN, exc)

                # Clean up and reconnect if allowed
                await self._cleanup()
                if not self._reconnect:
                    _LOGGER.info("[%s] Reconnect disabled — stopping client", DOMAIN)
                    break

                _LOGGER.warning("[%s] Disconnected — reconnecting in %s s", DOMAIN, delay)
                await asyncio.sleep(delay)
                delay = min(delay * self.BACK_OFF, self.MAX_RETRY_SEC)

            except asyncio.CancelledError:
                _LOGGER.info("[%s] Connection cancelled by user", DOMAIN)
                break
            except Exception as e:
                _LOGGER.warning("[%s] Connection error: %s — retrying in %s s", DOMAIN, e, delay)
                await asyncio.sleep(delay)
                delay = min(delay * self.BACK_OFF, self.MAX_RETRY_SEC)

    async def disconnect(self) -> None:
        """Close the connection, cancel tasks, and stop reconnection attempts."""
        self._reconnect = False
        _LOGGER.info("[%s] Disconnecting SignalR client", DOMAIN)
        await self._cleanup()
        _LOGGER.info("[%s] Disconnected cleanly", DOMAIN)

    async def _cleanup(self) -> None:
        """Internal: cancel tasks and close websocket."""
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()

        if self._ws:
            await self._ws.close()
            self._ws = None

    async def _negotiate(self) -> Tuple[Optional[str], Optional[str]]:
        """Perform the SignalR negotiation step to retrieve a connection token."""
        try:
            _LOGGER.debug("[%s] Negotiating SignalR connection…", DOMAIN)
            async with self._session.get(
                self.NEGOTIATION_URL,
                params={"clientProtocol": "1.5", "connectionData": HUB_DATA},
            ) as r:
                r.raise_for_status()
                data = await r.json()
                return data["ConnectionToken"], r.headers.get("Set-Cookie")

        except Exception as e:
            _LOGGER.error("[%s] Negotiation failed: %s", DOMAIN, e)
            return None, None

    async def _heartbeat(self) -> None:
        """Send periodic keep-alive messages to maintain connection."""
        try:
            while self.connected:
                await asyncio.sleep(self.HEARTBEAT)
                await self._ws.send_json(SUBSCRIBE_MSG)

                _LOGGER.debug("[%s] Sent heartbeat", DOMAIN)
        except asyncio.CancelledError:
            _LOGGER.debug("[%s] Heartbeat task cancelled", DOMAIN)
        except Exception:
            _LOGGER.exception("[%s] Heartbeat loop failed", DOMAIN)

    async def _listen(self) -> None:
        """Continuously listen for incoming websocket messages."""
        if not self._ws:
            _LOGGER.error("[%s] Listen loop started without active websocket", DOMAIN)
            return

        try:
            async for msg in self._ws:
                if msg.type == WSMsgType.TEXT:
                    payload = json.loads(msg.data)

                    for entry, data in payload.get("R", {}).items():
                        event_type = LiveTimingEvent.try_from(entry)
                        if not event_type:
                            _LOGGER.debug("[%s] Unknown event type: %s", DOMAIN, entry)
                            continue

                        parsed = EventFactory.parse(event_type, data)
                        if isinstance(parsed, Event):
                            _LOGGER.debug("[%s] Parsed event: %s", DOMAIN, event_type)
                            self.notify(parsed)

                elif msg.type in (WSMsgType.CLOSED, WSMsgType.ERROR):
                    _LOGGER.error("[%s] WebSocket closed or errored: %s", DOMAIN, msg.data)
                    break

        except asyncio.CancelledError:
            _LOGGER.debug("[%s] Listen task cancelled", DOMAIN)
        except Exception:
            _LOGGER.exception("[%s] Exception in listen loop", DOMAIN)
