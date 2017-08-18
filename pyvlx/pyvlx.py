"""
Module for PyVLX object.

PyVLX is an asynchronous library for connecting to
a VELUX KLF 200 device for controlling window openers
and roller shutters.
"""
import logging

from .config import Config
from .interface import Interface
from .devices import Devices
from .scenes import Scenes


class PyVLX:
    """Class for PyVLX."""

    def __init__(self, path=None, host=None, password=None):
        """Initialize PyVLX class."""
        self.logger = logging.getLogger('pyvlx.log')
        self.config = Config(self, path, host, password)
        self.interface = Interface(self.config)
        self.devices = Devices(self)
        self.scenes = Scenes(self)

    async def connect(self):
        """Connect to KLF 200."""
        await self.interface.refresh_token()

    async def disconnect(self):
        """Disconnect from KLF 200."""
        await self.interface.disconnect()

    async def load_devices(self):
        """Load devices from KLF 200."""
        await self.devices.load()

    async def load_scenes(self):
        """Load scenes from KLF 200."""
        await self.scenes.load()
