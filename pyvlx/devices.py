import json
from .device import Device
from .window import Window
from .rollershutter import RollerShutter
from .exception import PyVLXException

class Devices:

    def __init__(self, pyvlx):
        self.pyvlx = pyvlx
        self.__devices = []


    def __iter__(self):
        yield from self.__devices


    def __getitem__(self, key):
        for device in self.__devices:
            if device.name == key:
                return device

        if isinstance(key, int):
            return self.__devices[key]
        raise KeyError


    def __len__(self):
        return len(self.__devices)


    def add(self, device):
        if not isinstance(device, Device):
            raise TypeError()
        self.__devices.append(device)


    async def load(self):
        json_response = await self.pyvlx.interface.api_call('products', 'get')
        self.data_import(json_response)


    def data_import(self, json_response):
        if not 'data' in json_response:
            raise PyVLXException('no element data found in response: {0}'.format(json.dumps(json_response)))
        data = json_response['data']

        for item in data:
            if not 'category' in item:
                raise PyVLXException('no element category in product: {0}'.format(json.dumps(item)))
            category = item['category']
            if category == 'Window opener':
                self.load_window_opener(item)
            elif category == 'Roller shutter':
                self.load_roller_shutter(item)
            else:
                print('WARNING: Could not parse product: {0}'.format(category))


    def load_window_opener(self, item):
        window = Window.from_config(self.pyvlx, item)
        self.add(window)


    def load_roller_shutter(self, item):
        rollershutter = RollerShutter.from_config(self.pyvlx, item)
        self.add(rollershutter)
