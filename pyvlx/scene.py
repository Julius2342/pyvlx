from .device import Device

class Scene:

    def __init__(self, pyvlx, id, name):
        self.pyvlx = pyvlx
        self.id = id
        self.name = name


    @classmethod
    def from_config(cls, pyvlx, item):
        name = item['name']
        id = item['id']
        return cls(pyvlx, id, name)


    async def run(self):
        await self.pyvlx.interface.api_call('scenes','run', {'id':self.id})


    def __str__(self):
        return '<Scene name="{0}" ' \
                    'id="{1}" />' \
                    .format(
                        self.name,
                        self.id)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__



