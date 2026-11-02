"""
Module for PyVLX object.

PyVLX is an asynchronous library for connecting to
a VELUX KLF 200 device for controlling window openers
and roller shutters.
"""
import asyncio
import time
from datetime import datetime, timedelta

try:
    from ._version import version as v
except ImportError:
    v = "unknown"
from .api import get_limitation
from .api.frames import FrameBase
from .config import Config
from .connection import Connection
from .const import LimitationType
from .exception import PyVLXException
from .heartbeat import Heartbeat
from .klf200gateway import Klf200Gateway
from .log import PYVLXLOG
from .node_updater import NodeUpdater
from .nodes import Nodes
from .scenes import Scenes


class PyVLX:
    """Class for PyVLX."""

    def __init__(
        self,
        path: str | None = None,
        host: str | None = None,
        password: str | None = None,
        heartbeat_interval: int = 30,
        heartbeat_load_all_states: bool = True,
        *,
        heartbeat_quiet_period: float = 60.0,
    ):
        """Initialize PyVLX class."""
        if heartbeat_quiet_period < 0:
            heartbeat_quiet_period = 0.0
        self.heartbeat_quiet_period = heartbeat_quiet_period
        self._heartbeat_quiet_until: float = time.monotonic()
        self.config = Config(self, path, host, password)
        self.connection = Connection(config=self.config)
        self.heartbeat = Heartbeat(
            pyvlx=self,
            interval=heartbeat_interval,
            load_all_states=heartbeat_load_all_states,
        )
        self.node_updater = NodeUpdater(pyvlx=self)
        self.nodes = Nodes(self)
        self.connection.register_frame_received_cb(self.node_updater.process_frame)

        self.scenes = Scenes(self)
        self.version = None
        self.protocol_version = None
        self.klf200 = Klf200Gateway(pyvlx=self)
        self.api_call_semaphore = asyncio.Semaphore(1)  # Limit parallel commands
        PYVLXLOG.debug("Initialized pyvlx %s", v)

    async def connect(self) -> None:
        """Connect to KLF 200."""
        PYVLXLOG.debug("Connecting to KLF 200")
        await self.connection.connect()
        assert self.config.password is not None
        await self.klf200.password_enter(password=self.config.password)
        await self.klf200.get_version()
        await self.klf200.get_protocol_version()
        PYVLXLOG.debug(
            "Connected to: %s,  %s",
            str(self.klf200.version),
            str(self.klf200.protocol_version),
        )
        await self.klf200.house_status_monitor_disable(pyvlx=self)
        await self.klf200.get_state()
        await self.klf200.set_utc()
        await self.klf200.get_network_setup()
        await self.klf200.house_status_monitor_enable(pyvlx=self)
        await self.heartbeat.start()

    async def reboot_gateway(self) -> None:
        """For Compatibility: Reboot the KLF 200."""
        if not self.get_connected():
            PYVLXLOG.warning("KLF 200 reboot initiated, but gateway is not connected")
        else:
            PYVLXLOG.warning("KLF 200 reboot initiated")
            await self.klf200.reboot()

    def get_connected(self) -> bool:
        """Return whether the gateway is currently connected."""
        return self.connection.connected

    async def ensure_connected(self) -> None:
        """Check we're connected, and if not, connect."""
        if not self.connection.connected:
            await self.connect()

    async def send_frame(self, frame: FrameBase) -> None:
        """Send frame to API via connection."""
        await self.ensure_connected()
        self.connection.write(frame)

    def _mark_user_command_dispatched(self) -> None:
        """Extend the heartbeat quiet period after dispatching a user command."""
        if self.heartbeat_quiet_period > 0:
            quiet_until_walltime = datetime.now().astimezone() + timedelta(seconds=self.heartbeat_quiet_period)
            PYVLXLOG.debug(
                "User command dispatched, extending heartbeat quiet period by %ss until %s",
                self.heartbeat_quiet_period,
                quiet_until_walltime.isoformat(),
            )
            self._heartbeat_quiet_until = time.monotonic() + self.heartbeat_quiet_period

    @property
    def heartbeat_quiet_period_active(self) -> bool:
        """Return whether automatic heartbeat position polling should be paused."""
        return time.monotonic() < self._heartbeat_quiet_until

    async def disconnect(self) -> None:
        """Disconnect from KLF 200."""
        await self.heartbeat.stop()
        if self.connection.connected:
            try:
                # If the connection will be closed while house status monitor is enabled, a reconnection will fail on SSL handshake.
                if self.klf200.house_status_monitor_enabled:
                    await self.klf200.house_status_monitor_disable(pyvlx=self, timeout=5)
                # Reboot KLF200 when disconnecting to avoid unresponsive KLF200.
                await self.klf200.reboot()
            except (OSError, PyVLXException):
                PYVLXLOG.exception("Error during disconnect preparations")
            self.connection.disconnect()
            if self.connection.tasks:
                await asyncio.gather(*self.connection.tasks)  # Wait for all tasks to finish

    async def load_nodes(self, node_id: int | None = None) -> None:
        """Load devices from KLF 200, if no node_id is specified all nodes are loaded."""
        await self.nodes.load(node_id)

    async def load_scenes(self) -> None:
        """Load scenes from KLF 200."""
        await self.scenes.load()

    async def get_limitation(self, node_id: int) -> None:
        """Return limitation."""
        limit = get_limitation.GetLimitation(self, node_id, limitation_type=LimitationType.MIN_LIMITATION)
        await limit.do_api_call()
        limit = get_limitation.GetLimitation(self, node_id, limitation_type=LimitationType.MAX_LIMITATION)
        await limit.do_api_call()
