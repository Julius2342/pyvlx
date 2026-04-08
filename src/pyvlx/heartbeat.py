"""Module for sending get state requests to API in regular periods."""
import asyncio
from contextlib import suppress
from typing import TYPE_CHECKING

from .api import GetState
from .api.status_request import StatusRequest
from .exception import PyVLXException
from .log import PYVLXLOG
from .opening_device import Blind, DualRollerShutter

if TYPE_CHECKING:
    from pyvlx import PyVLX


class Heartbeat:
    """Class for sending heartbeats to API."""

    def __init__(
        self, pyvlx: "PyVLX", interval: int = 30, load_all_states: bool = True
    ):
        """Initialize Heartbeat object."""
        PYVLXLOG.debug("Heartbeat: initialize")
        self.pyvlx = pyvlx
        self.interval = interval
        self.load_all_states = load_all_states
        self.heartbeat_task: asyncio.Task[None] | None = None
        self._lock = asyncio.Lock()

    async def _run(self) -> None:
        PYVLXLOG.debug("Heartbeat: started")
        while True:
            PYVLXLOG.debug("Heartbeat: sleeping")
            await asyncio.sleep(self.interval)
            PYVLXLOG.debug("Heartbeat: pulsing")
            try:
                await self.pulse()
            except (OSError, PyVLXException) as e:
                PYVLXLOG.debug("Heartbeat: pulsing failed: %s", e)

    async def start(self) -> None:
        """Start heartbeat. Does nothing if already running."""
        async with self._lock:
            if self.heartbeat_task is not None and not self.heartbeat_task.done():
                PYVLXLOG.debug("Heartbeat: already running")
                return
            if self.heartbeat_task is not None and self.heartbeat_task.done():
                if not self.heartbeat_task.cancelled():
                    exc = self.heartbeat_task.exception()
                    if exc is not None:
                        PYVLXLOG.warning("Heartbeat: previous task died: %s", exc)
            PYVLXLOG.debug("Heartbeat: starting")
            self.heartbeat_task = asyncio.create_task(self._run())

    @property
    def stopped(self) -> bool:
        """Return Heartbeat running state."""
        return self.heartbeat_task is None or self.heartbeat_task.done()

    async def stop(self) -> None:
        """Stop heartbeat."""
        async with self._lock:
            task = self.heartbeat_task
            self.heartbeat_task = None
        if task is None:
            PYVLXLOG.debug("Heartbeat: was not running")
            return

        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        PYVLXLOG.debug("Heartbeat: stopped")

    async def pulse(self) -> None:
        """Send get state request to API to keep the connection alive."""
        PYVLXLOG.debug("Heartbeat: pulse")
        get_state = GetState(pyvlx=self.pyvlx)
        await get_state.do_api_call()
        if not get_state.success:
            raise PyVLXException("Unable to send get state.")

        # If nodes contain Blind or DualRollerShutter device, refresh orientation or upper/lower curtain positions because House Monitoring
        # delivers wrong values for FP1, FP2 and FP3 parameter
        for node in self.pyvlx.nodes:
            if isinstance(node, (Blind, DualRollerShutter)) or self.load_all_states:
                status_request = StatusRequest(self.pyvlx, node.node_id)
                await status_request.do_api_call()
                # give user requests a chance
                await asyncio.sleep(0.5)
