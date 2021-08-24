"""
Module for PyVLX object.

PyVLX is an asynchronous library for connecting to
a VELUX KLF 200 device for controlling window openers
and roller shutters.
"""
import asyncio

from .api import (
    get_limitation, house_status_monitor_disable, house_status_monitor_enable)
from .config import Config
from .connection import Connection
from .heartbeat import Heartbeat
from .klf200gateway import Klf200Gateway
from .log import PYVLXLOG
from .node_updater import NodeUpdater
from .nodes import Nodes
from .scenes import Scenes


class PyVLX:
    """Class for PyVLX."""

    def __init__(self, path=None, host=None, password=None, loop=None):
        """Initialize PyVLX class."""
        self.loop = loop or asyncio.get_event_loop()
        self.config = Config(self, path, host, password)
        self.connection = Connection(loop=self.loop, config=self.config)
        self.heartbeat = Heartbeat(pyvlx=self)
        self.node_updater = NodeUpdater(pyvlx=self)
        self.heartbeat.start()
        self.connection.register_frame_received_cb(self.node_updater.process_frame)
        self.nodes = Nodes(self)
        self.scenes = Scenes(self)
        self.version = None
        self.protocol_version = None
        self.klf200 = Klf200Gateway(pyvlx=self)

    async def connect(self):
        """Connect to KLF 200."""
        PYVLXLOG.debug("Connecting to KLF 200.")
        await self.connection.connect()
        await self.klf200.password_enter(password=self.config.password)
        await self.klf200.get_version()
        await self.klf200.get_protocol_version()
        PYVLXLOG.debug(
            "Connected to: %s,  %s",
            str(self.klf200.version),
            str(self.klf200.protocol_version)
        )

        await self.klf200.get_state()
        await self.klf200.set_utc()
        await self.klf200.get_network_setup()
        await house_status_monitor_enable(pyvlx=self)

    async def reboot_gateway(self):
        """For Compatibility: Reboot the KLF 200."""
        PYVLXLOG.warning("KLF 200 reboot initiated")
        await self.klf200.reboot()

    async def send_frame(self, frame):
        """Send frame to API via connection."""
        if not self.connection.connected:
            await self.connect()
        self.connection.write(frame)

    async def disconnect(self):
        """Disconnect from KLF 200."""
        # If the connection will be closed while house status monitor is enabled, a reconnection will fail on SSL handshake.
        await house_status_monitor_disable(pyvlx=self)
        await self.heartbeat.stop()
        self.connection.disconnect()

    async def load_nodes(self, node_id=None):
        """Load devices from KLF 200, if no node_id is specified all nodes are loaded."""
        await self.nodes.load(node_id)

    async def load_scenes(self):
        """Load scenes from KLF 200."""
        await self.scenes.load()

    async def get_limitation(self, node_id):
        limit = get_limitation.GetLimitation(self, [node_id])
        await limit.do_api_call()
