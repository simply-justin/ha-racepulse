import asyncio
import logging
from typing import Any, Dict
from aiohttp import ClientSession, WSMsgType, ClientWebSocketResponse
from .interfaces import Event, Notifiable, Observable
from .event_factory import EventFactory
from .decorators import _EVENT_REGISTRY


_LOGGER = logging.getLogger(__name__)

HUB_DATA = '[{"name":"Streaming"}]'
SUBSCRIBE_MSG = {
    "H": "Streaming",
    "M": "Subscribe",
    "A": [list(_EVENT_REGISTRY.keys())],
    "I": 1,
}


class F1SignalRClient(Notifiable):
    CONNECTION_URL = "wss://livetiming.formula1.com/signalr/connect"
    NEGOTIATION_URL = "https://livetiming.formula1.com/signalr/negotiate"
    FAST_RETRY_SEC = 5
    MAX_RETRY_SEC = 60
    BACK_OFF = 2
    HEARTBEAT = 300

    def __init__(self, session: ClientSession):
        self._session = session
        self._observers: list[Observable] = []
        self.state: Dict[str, object] = {}
        self._ws: ClientWebSocketResponse | None = None
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
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, message: "Event") -> None:
        for observer in self._observers:
            try:
                observer.update(self, message)
            except Exception:
                _LOGGER.exception("Failed to notify observer %s", observer)

    # ---------------- Connection ----------------
    async def connect(self) -> None:
        delay = self.FAST_RETRY_SEC
        while True:
            try:
                token, cookie = await self._negotiate()
                headers = {"User-Agent": "BestHTTP", "Accept-Encoding": "gzip,identity"}
                if cookie:
                    headers["Cookie"] = cookie
                params = {
                    "transport": "webSockets",
                    "clientProtocol": "1.5",
                    "connectionToken": token,
                    "connectionData": [HUB_DATA],
                }
                self._ws = await self._session.ws_connect(
                    self.CONNECTION_URL, params=params, headers=headers
                )
                await self._ws.send_json(SUBSCRIBE_MSG)
                self._tasks = [
                    asyncio.create_task(self._heartbeat()),
                    asyncio.create_task(self._listen()),
                ]
                _LOGGER.info("F1 client connected")
                return
            except Exception as e:
                _LOGGER.warning("Connect failed (%s). Retrying in %s sec", e, delay)
                await asyncio.sleep(delay)
                delay = min(delay * self.BACK_OFF, self.MAX_RETRY_SEC)

    async def disconnect(self) -> None:
        for t in self._tasks:
            t.cancel()
        self._tasks.clear()
        if self._ws:
            await self._ws.close()
            self._ws = None

    async def _negotiate(self) -> tuple[str, str | None]:
        async with self._session.get(self.NEGOTIATION_URL) as r:
            r.raise_for_status()
            data = await r.json()
            return data["ConnectionToken"], r.headers.get("Set-Cookie")

    async def _heartbeat(self) -> None:
        try:
            while self.connected:
                await asyncio.sleep(self.HEARTBEAT)
                await self._ws.send_json(SUBSCRIBE_MSG)
        except asyncio.CancelledError:
            pass
        except Exception:
            _LOGGER.exception("Heartbeat failed")

    async def _listen(self) -> None:
        try:
            async for msg in self._ws:
                if msg.type == WSMsgType.TEXT:
                    raw = msg.json(
                        loads=None
                    )  # server sends single object or array; adapt if array
                    self._handle_raw(raw)
                elif msg.type == WSMsgType.ERROR:
                    _LOGGER.error("WebSocket error: %s", msg.data)
                    break
        except asyncio.CancelledError:
            pass
        except Exception:
            _LOGGER.exception("Listen failed")

    # ---- event handling ----
    def _handle_raw(self, raw: Any) -> None:
        # If the server sometimes batches events in a list, handle both:
        items = raw if isinstance(raw, list) else [raw]
        for item in items:
            event = EventFactory.parse(item)
            # Store by enum string if available, else class name
            key = getattr(event, "data_type", None)
            if hasattr(key, "value"):  # LiveTimingEvent
                self.state[key.value] = event
            else:
                self.state[event.__class__.__name__] = event
            self.notify(event)
