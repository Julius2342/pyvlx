
class Scene:

    def __init__(self, pyvlx, ident, name):
        self.pyvlx = pyvlx
        self.ident = ident
        self.name = name


    @classmethod
    def from_config(cls, pyvlx, item):
        name = item['name']
        ident = item['id']
        return cls(pyvlx, ident, name)


    async def run(self):
        await self.pyvlx.interface.api_call('scenes', 'run', {'id': self.ident})


    def __str__(self):
        return '<Scene name="{0}" ' \
                    'id="{1}" />' \
                    .format(
                        self.name,
                        self.ident)


    def __eq__(self, other):
        return self.__dict__ == other.__dict__
