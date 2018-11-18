"""Module for window openers."""

from .device import Device


class Window(Device):
    """Class for window openers."""

    # pylint: disable=too-many-arguments
    def __init__(self, pyvlx, ident, name, subtype, typeid):
        """Initialize Window class."""
        self.pyvlx = pyvlx
        self.ident = ident
        self.name = name
        self.subtype = subtype
        self.typeid = typeid
        Device.__init__(self, pyvlx, ident, name)

    @classmethod
    def from_config(cls, pyvlx, item):
        """Read window opener from configuration."""
        name = item['name']
        ident = item['id']
        subtype = item['subtype']
        typeid = item['typeId']
        return cls(pyvlx, ident, name, subtype, typeid)

    def __str__(self):
        """Return object as readable string."""
        return '<Window name="{0}" ' \
            'id="{1}" ' \
            'subtype="{2}" ' \
            'typeId="{3}" />' \
            .format(
                self.name,
                self.ident,
                self.subtype,
                self.typeid)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
