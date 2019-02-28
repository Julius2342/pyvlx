"""Module for window openers."""
from .command_send import CommandSend
from .exception import PyVLXException
from .node import Node
from .parameter import CurrentPosition, Position


class OpeningDevice(Node):
    """Meta class for opening device with one main parameter for position."""

    def __init__(self, pyvlx, node_id, name):
        """Initialize opening device.

        Parameters:
            * pyvlx: PyVLX object
            * node_id: internal id for addressing nodes.
                Provided by KLF 200 device
            * name: node name

        """
        super().__init__(pyvlx=pyvlx, node_id=node_id, name=name)
        self.position = Position()

    async def set_position(self, position, wait_for_completion=True):
        """Set window to desired position.

        Parameters:
            * position: Position object containing the target position.
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        command_send = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=position)
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        await self.after_update()

    async def open(self, wait_for_completion=True):
        """Open window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=0),
            wait_for_completion=wait_for_completion)

    async def close(self, wait_for_completion=True):
        """Close window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=100),
            wait_for_completion=wait_for_completion)

    async def stop(self, wait_for_completion=True):
        """Stop window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=CurrentPosition(),
            wait_for_completion=wait_for_completion)


class Window(OpeningDevice):
    """Window object."""

    def __init__(self, pyvlx, node_id, name, rain_sensor=False):
        """Initialize Window class.

        Parameters:
            * pyvlx: PyVLX object
            * node_id: internal id for addressing nodes.
                Provided by KLF 200 device
            * name: node name
            * rain_sensor: set if device is equipped with a
                rain sensor.

        """
        super().__init__(pyvlx=pyvlx, node_id=node_id, name=name)
        self.rain_sensor = rain_sensor

    def __str__(self):
        """Return object as readable string."""
        return '<{} name="{}" ' \
            'node_id="{}" rain_sensor={}/>' \
            .format(
                type(self).__name__,
                self.name,
                self.node_id, self.rain_sensor)


class Blind(OpeningDevice):
    """Blind objects."""


class Awning(OpeningDevice):
    """Awning objects."""


class RollerShutter(OpeningDevice):
    """RollerShutter object."""
