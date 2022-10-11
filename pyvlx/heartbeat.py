"""Module for sending get state requests to API in regular periods."""
import asyncio

from .api import GetState
from .api.status_request import StatusRequest
from .log import PYVLXLOG
from .exception import PyVLXException
from .opening_device import Blind


class Heartbeat:
    """Class for sending heartbeats to API."""

    def __init__(self, pyvlx, timeout_in_seconds=30):
        """Initialize Heartbeat object."""
        PYVLXLOG.debug("Heartbeat __init__")
        self.pyvlx = pyvlx
        self.timeout_in_seconds = timeout_in_seconds
        self.task = None

    async def _run(self):
        PYVLXLOG.debug("Heartbeat: task started")
        while True:
            PYVLXLOG.debug("Heartbeat: sleeping")
            await asyncio.sleep(self.timeout_in_seconds)
            PYVLXLOG.debug("Heartbeat: pulsing")
            try:
                await self.pulse()
            except Exception as e:
                PYVLXLOG.debug("Heartbeat: pulsing failed: %s" % str(e))

    async def _start(self):
        if self.task is not None:
            self.stop()
        PYVLXLOG.debug("Heartbeat: creating task")
        self.task = asyncio.create_task(self._run())

    def start(self):
        PYVLXLOG.debug("Heartbeat start")
        asyncio.run_coroutine_threadsafe(self._start(), self.pyvlx.loop)

    @property
    def stopped(self):
        return self.task is None

    async def stop(self):
        """Stop heartbeat."""
        if self.task is not None:
            self.task.cancel()
            self.task = None
            PYVLXLOG.debug("Heartbeat stopped")
        else:
            PYVLXLOG.debug("Heartbeat was not running")

    async def pulse(self):
        """Send get state request to API to keep the connection alive."""
        PYVLXLOG.debug("Heartbeat pulse")
        get_state = GetState(pyvlx=self.pyvlx)
        await get_state.do_api_call()
        if not get_state.success:
            raise PyVLXException("Unable to send get state.")

        # If nodes contain Blind device, refresh orientation because House Monitoring
        # delivers wrong values for FP3 parameter
        for node in self.pyvlx.nodes:
            if isinstance(node, Blind):
                status_request = StatusRequest(self.pyvlx, node.node_id)
                await status_request.do_api_call()
