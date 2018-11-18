"""Module for storing devices."""

import json
from .device import Device
from .window import Window
from .rollershutter import RollerShutter
from .blind import Blind
from .exception import PyVLXException


class Devices:
    """Object for storing devices."""

    def __init__(self, pyvlx):
        """Initialize Devices class."""
        self.pyvlx = pyvlx
        self.__devices = []

    def __iter__(self):
        """Iterator."""
        yield from self.__devices

    def __getitem__(self, key):
        """Return device by name or by index."""
        for device in self.__devices:
            if device.name == key:
                return device
        if isinstance(key, int):
            return self.__devices[key]
        raise KeyError

    def __len__(self):
        """Return number of devices."""
        return len(self.__devices)

    def add(self, device):
        """Add device."""
        if not isinstance(device, Device):
            raise TypeError()
        self.__devices.append(device)

    async def load(self):
        """Load devices from KLF 200."""
        json_response = await self.pyvlx.interface.api_call('products', 'get')
        self.data_import(json_response)

    def data_import(self, json_response):
        """Import data from json response."""
        if 'data' not in json_response:
            raise PyVLXException('no element data found: {0}'.format(
                json.dumps(json_response)))
        data = json_response['data']

        for item in data:
            if 'category' not in item:
                raise PyVLXException('no element category: {0}'.format(
                    json.dumps(item)))
            category = item['category']
            if category == 'Window opener':
                self.load_window_opener(item)
            elif category in ['Roller shutter', 'Dual Shutter']:
                self.load_roller_shutter(item)
            elif category in ['Blind']:
                self.load_blind(item)
            else:
                self.pyvlx.logger.warning(
                    'WARNING: Could not parse product: %s', category)

    def load_window_opener(self, item):
        """Load window opener from JSON."""
        window = Window.from_config(self.pyvlx, item)
        self.add(window)

    def load_roller_shutter(self, item):
        """Load roller shutter from JSON."""
        rollershutter = RollerShutter.from_config(self.pyvlx, item)
        self.add(rollershutter)

    def load_blind(self, item):
        """Load blind from JSON."""
        blind = Blind.from_config(self.pyvlx, item)
        self.add(blind)
