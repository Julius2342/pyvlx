"""Module for roller shutters."""

from .device import Device


class RollerShutter(Device):
    """Class for roller shutters."""

    def __init__(self, pyvlx, ident, name, subtype, typeid):
        """Initialize roller shutter class."""
        self.pyvlx = pyvlx
        self.ident = ident
        self.name = name
        self.subtype = subtype
        self.typeid = typeid
        Device.__init__(self, pyvlx, ident, name)

    @classmethod
    def from_config(cls, pyvlx, item):
        """Read roller shutter from config."""
        name = item['name']
        ident = item['id']
        subtype = item['subtype']
        typeid = item['typeId']
        return cls(pyvlx, ident, name, subtype, typeid)

    def __str__(self) -> str:
        """Return object as readable string."""
        return '<RollerShutter name="{0}" ' \
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
