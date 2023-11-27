"""Base class for waiting for a specific answer frame from velux ap.."""
import asyncio
from typing import TYPE_CHECKING, Optional

from .frames import FrameBase

if TYPE_CHECKING:
    from pyvlx import PyVLX


class ApiEvent:
    """Base class for waiting a specific frame from API connection."""

    def __init__(self, pyvlx: "PyVLX", timeout_in_seconds: int = 10):
        """Initialize ApiEvent."""
        self.pyvlx = pyvlx
        self.response_received_or_timeout = asyncio.Event()

        self.success = False
        self.timeout_in_seconds = timeout_in_seconds
        self.timeout_callback = None
        self.timeout_handle: Optional[asyncio.TimerHandle] = None

    async def do_api_call(self) -> None:
        """Start. Sending and waiting for answer."""
        # We check for connection before entering the semaphore section
        # because otherwise we might try to connect, which calls this, and we get stuck on
        # the semaphore.
        await self.pyvlx.check_connected()

        async with self.pyvlx.api_call_semaphore:
            self.pyvlx.connection.register_frame_received_cb(self.response_rec_callback)
            await self.send_frame()
            await self.start_timeout()
            await self.response_received_or_timeout.wait()
            self.response_received_or_timeout.clear()
            await self.stop_timeout()
            self.pyvlx.connection.unregister_frame_received_cb(self.response_rec_callback)

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        raise NotImplementedError("handle_frame has to be implemented")

    async def send_frame(self) -> None:
        """Send frame to API connection."""
        await self.pyvlx.send_frame(self.request_frame())

    def request_frame(self) -> FrameBase:
        """Construct initiating frame."""
        raise NotImplementedError("send_frame has to be implemented")

    async def response_rec_callback(self, frame: FrameBase) -> None:
        """Handle frame. Callback from internal api connection."""
        if await self.handle_frame(frame):
            self.response_received_or_timeout.set()

    def timeout(self) -> None:
        """Handle timeout for not having received expected frame."""
        self.response_received_or_timeout.set()

    async def start_timeout(self) -> None:
        """Start timeout."""
        self.timeout_handle = self.pyvlx.connection.loop.call_later(
            self.timeout_in_seconds, self.timeout
        )

    async def stop_timeout(self) -> None:
        """Stop timeout."""
        if self.timeout_handle is not None:
            self.timeout_handle.cancel()
