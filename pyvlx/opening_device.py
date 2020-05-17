"""Module for window openers."""
from .command_send import CommandSend
from .exception import PyVLXException
from .node import Node
from .parameter import CurrentPosition, Parameter, Position, TargetPosition


class OpeningDevice(Node):
    """Meta class for opening device with one main parameter for position."""

    def __init__(
        self, pyvlx, node_id, name, serial_number, position_parameter=Parameter()
    ):
        """Initialize opening device.

        Parameters:
            * pyvlx: PyVLX object
            * node_id: internal id for addressing nodes.
                Provided by KLF 200 device
            * name: node name
            * serial_number: serial number of the node.
            * position_parameter: initial position of the opening device.

        """
        super().__init__(
            pyvlx=pyvlx, node_id=node_id, name=name, serial_number=serial_number
        )
        self.position = Position(parameter=position_parameter)

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
            parameter=position,
        )
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
            wait_for_completion=wait_for_completion,
        )

    async def close(self, wait_for_completion=True):
        """Close window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=100),
            wait_for_completion=wait_for_completion,
        )

    async def stop(self, wait_for_completion=True):
        """Stop window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=CurrentPosition(), wait_for_completion=wait_for_completion
        )

    def __str__(self):
        """Return object as readable string."""
        return (
            '<{} name="{}" '
            'node_id="{}" '
            'serial_number="{}" '
            'position="{}"/>'.format(
                type(self).__name__,
                self.name,
                self.node_id,
                self.serial_number,
                self.position,
            )
        )


class Window(OpeningDevice):
    """Window object."""

    def __init__(
        self,
        pyvlx,
        node_id,
        name,
        serial_number,
        position_parameter=Parameter(),
        rain_sensor=False,
    ):
        """Initialize Window class.

        Parameters:
            * pyvlx: PyVLX object
            * node_id: internal id for addressing nodes.
                Provided by KLF 200 device
            * name: node name
            * serial_number: serial number of the node.
            * position_parameter: initial position of the opening device.
            * rain_sensor: set if device is equipped with a
                rain sensor.

        """
        super().__init__(
            pyvlx=pyvlx,
            node_id=node_id,
            name=name,
            serial_number=serial_number,
            position_parameter=position_parameter,
        )
        self.rain_sensor = rain_sensor

    def __str__(self):
        """Return object as readable string."""
        return (
            '<{} name="{}" '
            'node_id="{}" rain_sensor={} '
            'serial_number="{}" position="{}"/>'.format(
                type(self).__name__,
                self.name,
                self.node_id,
                self.rain_sensor,
                self.serial_number,
                self.position,
            )
        )


class Blind(OpeningDevice):
    """Blind objects."""

    def __init__(
        self, pyvlx, node_id, name, serial_number, position_parameter=Parameter()
    ):
        """Initialize Blind class.

        Parameters:
            * pyvlx: PyVLX object
            * node_id: internal id for addressing nodes.
                Provided by KLF 200 device
            * name: node name

        """
        super().__init__(
            pyvlx=pyvlx,
            node_id=node_id,
            name=name,
            serial_number=serial_number,
            position_parameter=position_parameter,
        )
        self.orientation = Position(position_percent=0)
        self.target_orientation = TargetPosition()
        self.target_position = TargetPosition()

    async def set_position(self, position, wait_for_completion=True):
        """Set window to desired position.

        Parameters:
            * position: Position object containing the current position.
            * target_position: Position object holding the target position
                               which allows to ajust the position while the blind is in movement
                               without stopping the blind (if orientation position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        self.target_position = position
        self.position = position

        command_send = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=position,
            fp3=self.target_orientation,
        )
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
            wait_for_completion=wait_for_completion,
        )

    async def close(self, wait_for_completion=True):
        """Close window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position(
            position=Position(position_percent=100),
            wait_for_completion=wait_for_completion,
        )

    async def stop(self, wait_for_completion=True):
        """Stop Blind position."""
        await self.set_position(
            position=CurrentPosition(), wait_for_completion=wait_for_completion
        )

    async def set_orientation(self, orientation, wait_for_completion=True):
        """Set Blind shades to desired orientation.

        Parameters:
            * orientation: Position object containing the target orientation.
            + target_orientation: Position object holding the target orientation
                                  which allows to ajust the orientation while the blind is in movement
                                  without stopping the blind (if the position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        self.target_orientation = orientation
        self.orientation = orientation
        print("Orientation in device: %s " % (orientation))
        command_send = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=self.target_position,
            fp3=orientation,
        )
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        await self.after_update()
        # KLF200 always send UNKNOWN position for functional parameter, so orientation is set directly and not via GW_NODE_STATE_POSITION_CHANGED_NTF

    async def open_orientation(self, wait_for_completion=True):
        """Open Blind slats orientation.

        Blind slats with ±90° orientation are open at 50%
        """
        await self.set_orientation(
            orientation=Position(position_percent=50),
            wait_for_completion=wait_for_completion,
        )

    async def close_orientation(self, wait_for_completion=True):
        """Close Blind slats."""
        await self.set_orientation(
            orientation=Position(position_percent=100),
            wait_for_completion=wait_for_completion,
        )

    async def stop_orientation(self, wait_for_completion=True):
        """Stop Blind slats."""
        await self.set_orientation(
            orientation=CurrentPosition(), wait_for_completion=wait_for_completion
        )


class Awning(OpeningDevice):
    """Awning objects."""


class RollerShutter(OpeningDevice):
    """RollerShutter object."""


class GarageDoor(OpeningDevice):
    """GarageDoor object."""


class Gate(OpeningDevice):
    """Gate object."""


class Blade(OpeningDevice):
    """Blade object."""
