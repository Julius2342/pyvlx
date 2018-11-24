"""Base class for waiting for a specific answer frame from velux ap.."""
import asyncio


class ApiEvent():
    """Base class for waiting a specific frame from API connection."""

    def __init__(self, pyvlx, timeout_in_seconds=10):
        """Initialize ApiEvent."""
        self.pyvlx = pyvlx
        self.response_received_or_timeout = asyncio.Event()

        self.success = False
        self.timeout_in_seconds = timeout_in_seconds
        self.timeout_callback = None
        self.timeout_handle = None

    async def do_api_call(self):
        """Start. Sending and waiting for answer."""
        self.pyvlx.connection.register_frame_received_cb(
            self.response_rec_callback)
        await self.send_frame()
        await self.start_timeout()
        await self.response_received_or_timeout.wait()
        await self.stop_timeout()
        self.pyvlx.connection.unregister_frame_received_cb(self.response_rec_callback)

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        raise NotImplementedError('handle_frame has to be implemented')

    async def send_frame(self):
        """Send frame to API connection."""
        await self.pyvlx.send_frame(self.request_frame())

    def request_frame(self):
        """Construct initiating framw."""
        raise NotImplementedError('send_frame has to be implemented')

    async def response_rec_callback(self, frame):
        """Handle frame. Callback from internal api connection."""
        if await self.handle_frame(frame):
            self.response_received_or_timeout.set()

    def timeout(self):
        """Handle timeout for not having received expected frame."""
        self.response_received_or_timeout.set()

    async def start_timeout(self):
        """Start timeout."""
        self.timeout_handle = self.pyvlx.connection.loop.call_later(
            self.timeout_in_seconds, self.timeout)

    async def stop_timeout(self):
        """Stop timeout."""
        self.timeout_handle.cancel()
