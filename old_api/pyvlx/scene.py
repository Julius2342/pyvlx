"""Module for scene."""


class Scene:
    """Object for scene."""

    def __init__(self, pyvlx, ident, name):
        """Initialize Scene object."""
        self.pyvlx = pyvlx
        self.ident = ident
        self.name = name

    @classmethod
    def from_config(cls, pyvlx, item):
        """Read scene from configuration."""
        name = item['name']
        ident = item['id']
        return cls(pyvlx, ident, name)

    async def run(self):
        """Run scene."""
        await self.pyvlx.interface.api_call('scenes', 'run', {'id': self.ident})

    def get_name(self):
        """Return name of object."""
        return self.name

    def __str__(self):
        """Return object as readable string."""
        return '<Scene name="{0}" ' \
            'id="{1}" />' \
            .format(
                self.name,
                self.ident)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
