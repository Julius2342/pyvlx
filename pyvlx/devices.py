import json
from .device import Device
from .window import Window

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
        if not 'data' in json_response:
            raise Exception('no element data found in response: {0}'.format(json.dumps(json_response)))
        data = json_response['data']

        for item in data:
            if not 'category' in item:
                raise Exception('no element category in product: {0}'.format(json.dumps(item)))
            category = item['category']
            if category == 'Window opener':
                self.load_window_opener(item)
            else:
                print('WARNING: Could not parse product: {0}'.format(category))


    def load_window_opener(self, item):
        window = Window.from_config(self.pyvlx, item)
        self.add(window)
