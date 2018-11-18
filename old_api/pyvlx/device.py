"""
Module for basic object for devices.

Device objectis an interface class and should
be derived by other objects like window openers
and roller shutters.
"""


# pylint: disable=too-few-public-methods
class Device:
    """Class for device abstraction."""

    def __init__(self, pyvlx, ident, name):
        """Initialize Switch class."""
        self.pyvlx = pyvlx
        self.ident = ident
        self.name = name

    def get_name(self):
        """Return name of object."""
        return self.name
