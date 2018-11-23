"""Module for window openers."""
from .node import Node
from .command_send import CommandSend
from .position import Position
from .exception import PyVLXException


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

    async def set_position_percent(self, position_percent):
        """Set window to desired position."""
        command_send = CommandSend(pyvlx=self.pyvlx, node_id=self.node_id, position=Position(position_percent=position_percent))
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")

    async def open(self):
        """Open window."""
        await self.set_position_percent(0)

    async def close(self):
        """Close window."""
        await self.set_position_percent(100)
