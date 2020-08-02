"""Module for sending get state requests to API in regular periods."""
import asyncio

from .exception import PyVLXException
from .get_state import GetState
from .log import PYVLXLOG

class Heartbeat:
    """Class for sending heartbeats to API."""

    def __init__(self, pyvlx, timeout_in_seconds=60):
        """Initialize Heartbeat object."""
        self.pyvlx = pyvlx
        self.timeout_in_seconds = timeout_in_seconds
        self.loop_event = asyncio.Event()
        self.run_task = None
        self.timeout_handle = None

    def __del__(self):
        """Cleanup heartbeat."""
        self.stop()

    def start(self):
        """Create loop task."""
        self.run_task = self.pyvlx.loop.create_task(self.loop())

    def stop(self):
        """Stop heartbeat."""
        if self.timeout_handle is not None:
            self.timeout_handle.cancel()
            self.timeout_handle = None
        if self.run_task is not None:
            self.run_task.cancel()
            self.run_task = None

    async def loop(self):
        """Pulse every timeout seconds until stopped."""
        try:
            PYVLXLOG.debug("Heartbeat started")
            while True:
                self.timeout_handle = self.pyvlx.loop.call_later(
                    self.timeout_in_seconds, self.loop_event.set
                )
                await self.loop_event.wait()
                self.loop_event.clear()
                await self.pulse()
        except:
            PYVLXLOG.debug("Heartbeat stopped")
            raise

    async def pulse(self):
        """Send get state request to API to keep the connection alive."""
        get_state = GetState(pyvlx=self.pyvlx)
        await get_state.do_api_call()
        if not get_state.success:
            raise PyVLXException("Unable to send get state.")
