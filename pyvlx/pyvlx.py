from .config import Config
from .interface import Interface
from .devices import Devices
from .scenes import Scenes

class PyVLX:

    def __init__(self, path=None):
        self.config = Config(path)
        self.interface = Interface(self.config)
        self.devices = Devices(self)
        self.scenes = Scenes(self)


    async def connect(self):
        await self.interface.refresh_token()


    async def load_devices(self):
        await self.devices.load()


    async def load_scenes(self):
        await self.scenes.load()
