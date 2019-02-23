"""Module for handling the TCP connection with Gateway."""
import asyncio
import ssl

from .exception import PyVLXException
from .frame_creation import frame_from_raw
from .frames import FrameBase
from .log import PYVLXLOG
from .slip import get_next_slip, is_slip, slip_pack


class SlipTokenizer:
    """Helper class for splitting up binary stream to slip packets."""

    def __init__(self):
        """Init Tokenizer."""
        self.data = bytes()

    def feed(self, chunk):
        """Feed chunk to tokenizer."""
        if not chunk:
            return
        self.data += chunk

    def has_tokens(self):
        """Return True if Tokenizer has tokens."""
        return is_slip(self.data)

    def get_next_token(self):
        """Get next token from Tokenizer."""
        slip, self.data = get_next_slip(self.data)
        return slip


class TCPTransport(asyncio.Protocol):
    """Class for handling asyncio connection transport."""

    def __init__(self, frame_received_cb, connection_closed_cb):
        """Init TCPTransport."""
        self.frame_received_cb = frame_received_cb
        self.connection_closed_cb = connection_closed_cb
        self.tokenizer = SlipTokenizer()

    def connection_made(self, transport):
        """Handle sucessful connection."""

    def data_received(self, data):
        """Handle data received."""
        self.tokenizer.feed(data)
        while self.tokenizer.has_tokens():
            raw = self.tokenizer.get_next_token()
            frame = frame_from_raw(raw)
            if frame is not None:
                self.frame_received_cb(frame)

    def connection_lost(self, exc):
        """Handle lost connection."""
        self.connection_closed_cb()


class Connection:
    """Class for handling TCP connection."""

    def __init__(self, loop, config):
        """Init TCP connection."""
        self.loop = loop
        self.config = config
        self.transport = None
        self.frame_received_cbs = []
        self.connected = False

    def __del__(self):
        """Destruct connection."""
        self.disconnect()

    def disconnect(self):
        """Disconnect connection."""
        if self.transport is not None:
            self.transport.close()
            self.transport = None

    async def connect(self):
        """Connect to gateway via SSL."""
        tcp_client = TCPTransport(self.frame_received_cb, self.connection_closed_cb)
        self.transport, _ = await self.loop.create_connection(
            lambda: tcp_client,
            host=self.config.host,
            port=self.config.port,
            ssl=self.create_ssl_context())
        self.connected = True

    def register_frame_received_cb(self, callback):
        """Register frame received callback."""
        self.frame_received_cbs.append(callback)

    def unregister_frame_received_cb(self, callback):
        """Unregister frame received callback."""
        self.frame_received_cbs.remove(callback)

    def write(self, frame):
        """Write frame to Bus."""
        if not isinstance(frame, FrameBase):
            raise PyVLXException("Frame not of type FrameBase", frame_type=type(frame))
        PYVLXLOG.debug("SEND: %s", frame)
        self.transport.write(slip_pack(bytes(frame)))

    @staticmethod
    def create_ssl_context():
        """Create and return SSL Context."""
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        return ssl_context

    def frame_received_cb(self, frame):
        """Received message."""
        PYVLXLOG.debug("REC: %s", frame)
        for frame_received_cb in self.frame_received_cbs:
            # pylint: disable=not-callable
            self.loop.create_task(frame_received_cb(frame))

    def connection_closed_cb(self):
        """Server closed connection."""
        self.connected = False
