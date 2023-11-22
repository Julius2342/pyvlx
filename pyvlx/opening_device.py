"""Module for window openers."""
from typing import TYPE_CHECKING, Optional

from .api.command_send import CommandSend
from .api.get_limitation import GetLimitation
from .exception import PyVLXException
from .node import Node
from .parameter import (
    CurrentPosition, IgnorePosition, Parameter, Position, TargetPosition)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class OpeningDevice(Node):
    """Meta class for opening device with one main parameter for position."""

    def __init__(
            self, pyvlx: "PyVLX", node_id: int, name: str, serial_number: str, position_parameter: Parameter = Parameter()
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

    async def set_position(self, position: Position, wait_for_completion: bool = True) -> None:
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

    async def open(self, wait_for_completion: bool = True) -> None:
        """Open window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=0),
            wait_for_completion=wait_for_completion,
        )

    async def close(self, wait_for_completion: bool = True) -> None:
        """Close window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=100),
            wait_for_completion=wait_for_completion,
        )

    async def stop(self, wait_for_completion: bool = True) -> None:
        """Stop window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=CurrentPosition(), wait_for_completion=wait_for_completion
        )

    def __str__(self) -> str:
        """Return object as readable string."""
        return (
            '<{} name="{}" node_id="{}" serial_number="{}" position="{}"/>'.format(
                type(self).__name__, self.name, self.node_id, self.serial_number, self.position
            )
        )


class Window(OpeningDevice):
    """Window object."""

    def __init__(
            self,
            pyvlx: "PyVLX",
            node_id: int,
            name: str,
            serial_number: str,
            position_parameter: Parameter = Parameter(),
            rain_sensor: bool = False,
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

    def __str__(self) -> str:
        """Return object as readable string."""
        return (
            '<{} name="{}" node_id="{}" rain_sensor={} serial_number="{}" position="{}"/>'.format(
                type(self).__name__, self.name, self.node_id,
                self.rain_sensor, self.serial_number, self.position
            )
        )

    async def get_limitation(self) -> GetLimitation:
        """Return limitaation."""
        get_limitation = GetLimitation(pyvlx=self.pyvlx, node_id=self.node_id)
        await get_limitation.do_api_call()
        if not get_limitation.success:
            raise PyVLXException("Unable to send command")
        return get_limitation


class Blind(OpeningDevice):
    """Blind objects."""

    def __init__(
            self, pyvlx: "PyVLX", node_id: int, name: str, serial_number: str, position_parameter: Parameter = Parameter()
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
        self.open_orientation_target: int = 50
        self.close_orientation_target: int = 100

    async def set_position_and_orientation(self,
                                           position: Position,
                                           wait_for_completion: bool = True,
                                           orientation: Optional[Position] = None) -> None:
        """Set window to desired position.

        Parameters:
            * position: Position object containing the current position.
            * target_position: Position object holding the target position
                which allows to ajust the position while the blind is in movement
                without stopping the blind (if orientation position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.
            * orientation: If set, the orientation of the device will be set in the same request.
                Note, that, if the position is set to 0, the orientation will be set to 0 too.

        """
        self.target_position = TargetPosition.from_position(position)
        self.position = position

        fp3: Position
        if orientation is not None:
            fp3 = orientation
        elif self.target_position == Position(position_percent=0):
            fp3 = Position(position_percent=0)
        else:
            fp3 = IgnorePosition()

        command_send = CommandSend(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            parameter=position,
            wait_for_completion=wait_for_completion,
            fp3=fp3
        )
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        await self.after_update()

    async def set_position(self, position: Position, wait_for_completion: bool = True) -> None:
        """Set window to desired position.

        Parameters:
            * position: Position object containing the current position.
            * target_position: Position object holding the target position
                which allows to ajust the position while the blind is in movement
                without stopping the blind (if orientation position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position_and_orientation(position, wait_for_completion)

    async def open(self, wait_for_completion: bool = True) -> None:
        """Open window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position(
            position=Position(position_percent=0),
            wait_for_completion=wait_for_completion,
        )

    async def close(self, wait_for_completion: bool = True) -> None:
        """Close window.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position(
            position=Position(position_percent=100),
            wait_for_completion=wait_for_completion,
        )

    async def stop(self, wait_for_completion: bool = True) -> None:
        """Stop Blind position."""
        await self.set_position_and_orientation(
            position=CurrentPosition(), wait_for_completion=wait_for_completion, orientation=self.target_orientation
        )

    async def set_orientation(self, orientation: Position, wait_for_completion: bool = True) -> None:
        """Set Blind shades to desired orientation.

        Parameters:
            * orientation: Position object containing the target orientation.
            + target_orientation: Position object holding the target orientation
                which allows to adjust the orientation while the blind is in movement
                without stopping the blind (if the position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        self.target_orientation = TargetPosition.from_position(orientation)
        self.orientation = orientation

        fp3 = Position(position_percent=0)\
            if self.target_position == Position(position_percent=0)\
            else self.target_orientation

        print("Orientation in device: %s " % (orientation))
        command_send = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=IgnorePosition(),
            fp3=fp3,
        )
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        await self.after_update()
        # KLF200 always send UNKNOWN position for functional parameter,
        # so orientation is set directly and not via GW_NODE_STATE_POSITION_CHANGED_NTF

    async def open_orientation(self, wait_for_completion: bool = True) -> None:
        """Open Blind slats orientation.

        Blind slats with ±90° orientation are open at 50%
        """
        await self.set_orientation(
            orientation=Position(position_percent=self.open_orientation_target),
            wait_for_completion=wait_for_completion,
        )

    async def close_orientation(self, wait_for_completion: bool = True) -> None:
        """Close Blind slats."""
        await self.set_orientation(
            orientation=Position(position_percent=self.close_orientation_target),
            wait_for_completion=wait_for_completion,
        )

    async def stop_orientation(self, wait_for_completion: bool = True) -> None:
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
