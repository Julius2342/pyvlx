"""Module for handling the TCP connection with Gateway."""
import asyncio
import ssl
import sys
from typing import Callable, Coroutine, List, Optional, Set

from .api.frame_creation import frame_from_raw
from .api.frames import FrameBase
from .config import Config
from .exception import PyVLXException
from .log import PYVLXLOG
from .slip import get_next_slip, is_slip, slip_pack


class SlipTokenizer:
    """Helper class for splitting up binary stream to slip packets."""

    def __init__(self) -> None:
        """Init Tokenizer."""
        self.data = bytes()

    def feed(self, chunk: bytes) -> None:
        """Feed chunk to tokenizer."""
        if not chunk:
            return
        self.data += chunk

    def has_tokens(self) -> bool:
        """Return True if Tokenizer has tokens."""
        return is_slip(self.data)

    def get_next_token(self) -> Optional[bytes]:
        """Get next token from Tokenizer."""
        slip, self.data = get_next_slip(self.data)
        return slip


class TCPTransport(asyncio.Protocol):
    """Class for handling asyncio connection transport."""

    def __init__(
        self,
        frame_received_cb: Callable[[FrameBase], None],
        connection_lost_cb: Callable[[], None],
    ):
        """Init TCPTransport."""
        self.frame_received_cb = frame_received_cb
        self.connection_lost_cb = connection_lost_cb
        self.tokenizer = SlipTokenizer()

    def connection_made(self, transport: object) -> None:
        """Handle sucessful connection."""
        PYVLXLOG.debug("Socket connection to KLF 200 opened")

    def data_received(self, data: bytes) -> None:
        """Handle data received."""
        self.tokenizer.feed(data)
        while self.tokenizer.has_tokens():
            raw = self.tokenizer.get_next_token()
            assert raw is not None

            try:
                frame = frame_from_raw(raw)
                if frame is not None:
                    self.frame_received_cb(frame)
            except PyVLXException:
                PYVLXLOG.error("Error in data_received", exc_info=sys.exc_info())

    def connection_lost(self, exc: object) -> None:
        """Handle lost connection."""
        PYVLXLOG.debug("Socket connection to KLF 200 has been lost")
        self.connection_lost_cb()


CallbackType = Callable[[FrameBase], Coroutine]


class Connection:
    """Class for handling TCP connection."""

    def __init__(self, loop: asyncio.AbstractEventLoop, config: Config):
        """Init TCP connection."""
        self.loop = loop
        self.config = config
        self.transport: Optional[asyncio.Transport] = None
        self.frame_received_cbs: List[CallbackType] = []
        self.connection_closed_cbs: List[Callable[[], Coroutine]] = []
        self.connection_opened_cbs: List[Callable[[], Coroutine]] = []
        self.connected = False
        self.connection_counter = 0
        self.tasks: Set[asyncio.Task] = set()

    def __del__(self) -> None:
        """Destruct connection."""
        self.disconnect()

    def disconnect(self) -> None:
        """Disconnect connection."""
        if self.transport is not None:
            self.transport.close()
            self.transport = None
        self.connected = False
        PYVLXLOG.debug("TCP transport closed.")
        for connection_closed_cb in self.connection_closed_cbs:
            if asyncio.iscoroutine(connection_closed_cb()):
                task = self.loop.create_task(connection_closed_cb())
                self.tasks.add(task)
                task.add_done_callback(self.tasks.remove)

    async def connect(self) -> None:
        """Connect to gateway via SSL."""
        tcp_client = TCPTransport(self.frame_received_cb, connection_lost_cb=self.on_connection_lost)
        assert self.config.host is not None
        self.transport, _ = await self.loop.create_connection(
            lambda: tcp_client,
            host=self.config.host,
            port=self.config.port,
            ssl=self.create_ssl_context(),
        )
        self.connected = True
        self.connection_counter += 1
        PYVLXLOG.debug(
            "Amount of connections since last HA start: %s", self.connection_counter
        )
        for connection_opened_cb in self.connection_opened_cbs:
            if asyncio.iscoroutine(connection_opened_cb()):
                task = self.loop.create_task(connection_opened_cb())
                self.tasks.add(task)
                task.add_done_callback(self.tasks.remove)

    def register_frame_received_cb(self, callback: CallbackType) -> None:
        """Register frame received callback."""
        self.frame_received_cbs.append(callback)

    def unregister_frame_received_cb(self, callback: CallbackType) -> None:
        """Unregister frame received callback."""
        self.frame_received_cbs.remove(callback)

    def register_connection_closed_cb(self, callback: Callable[[], Coroutine]) -> None:
        """Register connection closed callback."""
        self.connection_closed_cbs.append(callback)

    def unregister_connection_closed_cb(self, callback: Callable[[], Coroutine]) -> None:
        """Unregister connection closed callback."""
        self.connection_closed_cbs.remove(callback)

    def register_connection_opened_cb(self, callback: Callable[[], Coroutine]) -> None:
        """Register connection opened callback."""
        self.connection_opened_cbs.append(callback)

    def unregister_connection_opened_cb(self, callback: Callable[[], Coroutine]) -> None:
        """Unregister connection opened callback."""
        self.connection_opened_cbs.remove(callback)

    def write(self, frame: FrameBase) -> None:
        """Write frame to Bus."""
        if not isinstance(frame, FrameBase):
            raise PyVLXException("Frame not of type FrameBase", *type(frame))
        PYVLXLOG.debug("SEND: %s", frame)
        assert self.transport is not None
        self.transport.write(slip_pack(bytes(frame)))

    @staticmethod
    def create_ssl_context() -> ssl.SSLContext:
        """Create and return SSL Context."""
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    def frame_received_cb(self, frame: FrameBase) -> None:
        """Received message."""
        PYVLXLOG.debug("REC: %s", frame)
        for frame_received_cb in self.frame_received_cbs:
            # pylint: disable=not-callable
            task = self.loop.create_task(frame_received_cb(frame))
            self.tasks.add(task)
            task.add_done_callback(self.tasks.remove)

    def on_connection_lost(self) -> None:
        """Server closed connection."""
        self.disconnect()
