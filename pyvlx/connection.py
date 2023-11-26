"""Module for handling the TCP connection with Gateway."""
import asyncio
import ssl
import sys
from typing import Callable, Coroutine, List, Optional

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
        connection_closed_cb: Callable[[], None],
    ):
        """Init TCPTransport."""
        self.frame_received_cb = frame_received_cb
        self.connection_closed_cb = connection_closed_cb
        self.tokenizer = SlipTokenizer()

    def connection_made(self, transport: object) -> None:
        """Handle sucessful connection."""

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
        self.connection_closed_cb()


CallbackType = Callable[[FrameBase], Coroutine]


class Connection:
    """Class for handling TCP connection."""

    def __init__(self, loop: asyncio.AbstractEventLoop, config: Config):
        """Init TCP connection."""
        self.loop = loop
        self.config = config
        self.transport: Optional[asyncio.Transport] = None
        self.frame_received_cbs: List[CallbackType] = []
        self.connected = False
        self.connection_counter = 0

    def __del__(self) -> None:
        """Destruct connection."""
        self.disconnect()

    def disconnect(self) -> None:
        """Disconnect connection."""
        if self.transport is not None:
            self.transport.close()
            self.transport = None
        self.connected = False

    async def connect(self) -> None:
        """Connect to gateway via SSL."""
        tcp_client = TCPTransport(self.frame_received_cb, self.connection_closed_cb)
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

    def register_frame_received_cb(self, callback: CallbackType) -> None:
        """Register frame received callback."""
        self.frame_received_cbs.append(callback)

    def unregister_frame_received_cb(self, callback: CallbackType) -> None:
        """Unregister frame received callback."""
        self.frame_received_cbs.remove(callback)

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
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    def frame_received_cb(self, frame: FrameBase) -> None:
        """Received message."""
        PYVLXLOG.debug("REC: %s", frame)
        for frame_received_cb in self.frame_received_cbs:
            # pylint: disable=not-callable
            self.loop.create_task(frame_received_cb(frame))

    def connection_closed_cb(self) -> None:
        """Server closed connection."""
        self.disconnect()
