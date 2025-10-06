import asyncio
import logging
from typing import TYPE_CHECKING, Any, Dict
from aiohttp import ClientSession, WSMsgType, ClientWebSocketResponse
from .interfaces import Event, Notifiable, Observable
from .event_factory import EventFactory
from .decorators import _EVENT_REGISTRY


if TYPE_CHECKING:
    from .interfaces import Event, Observable

_LOGGER = logging.getLogger(__name__)

HUB_DATA = '[{"name":"Streaming"}]'
SUBSCRIBE_MSG = {
    "H": "Streaming",
    "M": "Subscribe",
    "A": [list(_EVENT_REGISTRY.keys())],
    "I": 1,
}

# TODO: Implement Paid Logic. (Getting credentials from HA)
# TODO: Improve client
# TODO: Improve logging
# TODO: Improve parsing logic

class F1SignalRClient(Notifiable):
    CONNECTION_URL = "wss://livetiming.formula1.com/signalr/connect"
    NEGOTIATION_URL = "https://livetiming.formula1.com/signalr/negotiate"

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

    def notify(self, message: Event) -> None:
        for observer in self._observers:
            try:
                observer.update(self, message)
            except Exception:
                _LOGGER.exception("Failed to notify observer %s", observer)

    # ---------------- Connection ----------------
    async def connect() -> None:
        # NEgotiate a connection token.