"""
Module for PyVLX object.

PyVLX is an asynchronous library for connecting to
a VELUX KLF 200 device for controlling window openers
and roller shutters.
"""
import asyncio
from typing import Optional

from .api import get_limitation
from .api.frames import FrameBase
from .config import Config
from .connection import Connection
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
        path: Optional[str] = None,
        host: Optional[str] = None,
        password: Optional[str] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        heartbeat_interval: int = 30,
        heartbeat_load_all_states: bool = True,
    ):
        """Initialize PyVLX class."""
        self.loop = loop or asyncio.get_event_loop()
        self.config = Config(self, path, host, password)
        self.connection = Connection(loop=self.loop, config=self.config)
        self.heartbeat = Heartbeat(
            pyvlx=self,
            interval=heartbeat_interval,
            load_all_states=heartbeat_load_all_states,
        )
        self.node_updater = NodeUpdater(pyvlx=self)
        self.connection.register_frame_received_cb(self.node_updater.process_frame)
        self.nodes = Nodes(self)
        self.scenes = Scenes(self)
        self.version = None
        self.protocol_version = None
        self.klf200 = Klf200Gateway(pyvlx=self)
        self.api_call_semaphore = asyncio.Semaphore(1)  # Limit parallel commands
        PYVLXLOG.debug("Loadig pyvlx v0.2.21")

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
        self.heartbeat.start()

    async def reboot_gateway(self) -> None:
        """For Compatibility: Reboot the KLF 200."""
        PYVLXLOG.warning("KLF 200 reboot initiated")
        await self.klf200.reboot()

    async def check_connected(self) -> None:
        """Check we're connected, and if not, connect."""
        if not self.connection.connected:
            await self.connect()

    async def send_frame(self, frame: FrameBase) -> None:
        """Send frame to API via connection."""
        await self.check_connected()
        self.connection.write(frame)

    async def disconnect(self) -> None:
        """Disconnect from KLF 200."""
        # If the connection will be closed while house status monitor is enabled, a reconnection will fail on SSL handshake.
        try:
            await self.klf200.house_status_monitor_disable(pyvlx=self, timeout=1)
        except (OSError, PyVLXException):
            pass
        await self.heartbeat.stop()
        self.connection.disconnect()

    async def load_nodes(self, node_id: Optional[int] = None) -> None:
        """Load devices from KLF 200, if no node_id is specified all nodes are loaded."""
        await self.nodes.load(node_id)

    async def load_scenes(self) -> None:
        """Load scenes from KLF 200."""
        await self.scenes.load()

    async def get_limitation(self, node_id: int) -> None:
        """Return limitation."""
        limit = get_limitation.GetLimitation(self, node_id)
        await limit.do_api_call()
