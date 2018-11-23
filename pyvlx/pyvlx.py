"""
Module for PyVLX object.

PyVLX is an asynchronous library for connecting to
a VELUX KLF 200 device for controlling window openers
and roller shutters.
"""
import logging
import asyncio
from .config import Config
from .connection import Connection
from .login import Login
from .exception import PyVLXException
# from .devices import Devices
from .scenes import Scenes


class PyVLX:
    """Class for PyVLX."""

    # pylint: disable=too-many-arguments

    def __init__(self, path=None, host=None, password=None, log_frames=False, loop=None):
        """Initialize PyVLX class."""
        self.loop = loop or asyncio.get_event_loop()
        self.logger = logging.getLogger('pyvlx.log')
        self.config = Config(self, path, host, password)
        self.connection = Connection(loop=self.loop, config=self.config)
        if log_frames:
            self.connection.register_frame_received_cb(self.log_frame)
        # self.devices = Devices(self)
        self.scenes = Scenes(self)

    async def connect(self):
        """Connect to KLF 200."""
        await self.connection.connect()
        login = Login(connection=self.connection, password=self.config.password)
        await login.do_api_call()
        if not login.success:
            raise PyVLXException("Unable to login")

    async def disconnect(self):
        """Disconnect from KLF 200."""
        self.connection.disconnect()

    async def load_devices(self):
        """Load devices from KLF 200."""
        # await self.devices.load()
        pass

    async def load_scenes(self):
        """Load scenes from KLF 200."""
        await self.scenes.load()

    async def log_frame(self, frame):
        """Log frame to logger."""
        self.logger.warning("%s", frame)
