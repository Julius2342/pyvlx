"""Module for sending get state requests to API in regular periods."""
import asyncio
from typing import TYPE_CHECKING, Any

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
        PYVLXLOG.debug("Heartbeat __init__")
        self.pyvlx = pyvlx
        self.interval = interval
        self.load_all_states = load_all_states
        self.task: Any = None

    async def _run(self) -> None:
        PYVLXLOG.debug("Heartbeat: task started")
        while True:
            PYVLXLOG.debug("Heartbeat: sleeping")
            await asyncio.sleep(self.interval)
            PYVLXLOG.debug("Heartbeat: pulsing")
            try:
                await self.pulse()
            except (OSError, PyVLXException) as e:
                PYVLXLOG.debug("Heartbeat: pulsing failed: %s", e)

    async def _start(self) -> None:
        if self.task is not None:
            await self.stop()
        PYVLXLOG.debug("Heartbeat: creating task")
        self.task = asyncio.create_task(self._run())

    def start(self) -> None:
        """Start heartbeat."""
        PYVLXLOG.debug("Heartbeat start")
        asyncio.run_coroutine_threadsafe(self._start(), self.pyvlx.loop)

    @property
    def stopped(self) -> bool:
        """Return Heartbeat running state."""
        return self.task is None

    async def stop(self) -> None:
        """Stop heartbeat."""
        if self.task is not None:
            self.task.cancel()
            self.task = None
            PYVLXLOG.debug("Heartbeat stopped")
        else:
            PYVLXLOG.debug("Heartbeat was not running")

    async def pulse(self) -> None:
        """Send get state request to API to keep the connection alive."""
        PYVLXLOG.debug("Heartbeat pulse")
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
