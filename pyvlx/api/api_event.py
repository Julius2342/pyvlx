"""Base class for waiting for a specific answer frame from Velux API."""
import asyncio
from typing import TYPE_CHECKING

from .frames import FrameBase

if TYPE_CHECKING:
    from pyvlx import PyVLX


class ApiEvent:
    """Base class for waiting a specific frame from API connection.

    Objects of this class are single-use only, i.e. after one
    call to do_api_call() they must be discarded.
    """

    def __init__(self, pyvlx: "PyVLX", timeout_in_seconds: int = 10):
        """Initialize ApiEvent."""
        self.pyvlx = pyvlx
        self.response_received_or_timeout = asyncio.Event()

        self.success = False
        self.timeout_in_seconds = timeout_in_seconds

        self.used = False

    async def do_api_call(self) -> None:
        """Start. Sending and waiting for answer."""
        assert not self.used, "ApiEvent objects are single-use only"
        self.used = True

        # We check for connection before entering the semaphore section
        # because otherwise we might try to connect, which calls this, and we get stuck on
        # the semaphore.
        await self.pyvlx.check_connected()

        if self.pyvlx.get_connected():
            async with self.pyvlx.api_call_semaphore:
                self.pyvlx.connection.register_frame_received_cb(self.response_rec_callback)
                try:
                    await self.send_frame()
                    try:
                        async with asyncio.timeout(self.timeout_in_seconds):
                            await self.response_received_or_timeout.wait()

                    except TimeoutError:
                        self.success = False

                finally:
                    self.pyvlx.connection.unregister_frame_received_cb(self.response_rec_callback)
        else:
            self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming frame. Return True if this frame completes the API call.

        Note that the return value only indicates if the API call is completed,
        not if it was successful.
        The success attribute has to be checked for that.
        """
        raise NotImplementedError("handle_frame has to be implemented")

    async def send_frame(self) -> None:
        """Send frame to API connection."""
        await self.pyvlx.send_frame(self.request_frame())

    def request_frame(self) -> FrameBase:
        """Construct initiating frame."""
        raise NotImplementedError("request_frame has to be implemented")

    async def response_rec_callback(self, frame: FrameBase) -> None:
        """Handle frame. Callback from internal api connection."""
        if await self.handle_frame(frame):
            self.response_received_or_timeout.set()
