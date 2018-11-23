"""Module for window openers."""

from .node import Node


class Window(Node):
    """Class for window openers."""

    # pylint: disable=too-many-arguments
    def __init__(self, pyvlx, node_id, name, rain_sensor=False):
        """Initialize Window class."""
        Node.__init__(self, pyvlx=pyvlx, node_id=node_id, name=name)
        self.rain_sensor = rain_sensor

    def __str__(self):
        """Return object as readable string."""
        return '<Window name="{}" ' \
            'node_id="{}" rain_sensor={}/>' \
            .format(
                self.name,
                self.node_id, self.rain_sensor)

    async def open(self):
        """Open window."""
        print("Open window: ", self.name)

    async def close(self):
        """Close window."""
        print("Close window: ", self.name)
