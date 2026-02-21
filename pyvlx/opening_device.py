"""Module for Opening devices."""
import asyncio
import datetime
from asyncio import Task
from typing import TYPE_CHECKING, Any, Optional

from deprecated import deprecated

from pyvlx.api.get_limitation import GetLimitation

from .api.command_send import CommandSend
from .api.set_limitation import SetLimitation
from .const import LimitationType, Originator, Velocity
from .exception import PyVLXException
from .node import Node
from .parameter import (
    CurrentPosition, DualRollerShutterPosition, IgnorePosition, LimitationTime,
    LimitationTimeClearAll, Parameter, Position, TargetPosition)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class OpeningDevice(Node):
    """Meta class for opening device with one main parameter for position."""

    def __init__(
        self,
        pyvlx: "PyVLX",
        node_id: int,
        name: str,
        serial_number: Optional[str] = None,
        position_parameter: Parameter = Parameter(),
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
        self.position: Position = Position(parameter=position_parameter)
        self.target: Position = Position(parameter=position_parameter)
        self.limitation_min: Position = IgnorePosition()
        self.limitation_max: Position = IgnorePosition()
        self.limitation_time: LimitationTime = LimitationTimeClearAll()
        self.limitation_originator: Originator = Originator.USER

        self.is_opening: bool = False
        self.is_closing: bool = False
        self.state_received_at: Optional[datetime.datetime] = None
        self.estimated_completion: Optional[datetime.datetime] = None
        self.use_default_velocity: bool = False
        self.default_velocity: Velocity = Velocity.DEFAULT
        self.open_position_target: int = 0
        self.close_position_target: int = 100
        self._update_task: Task | None = None

    async def _update_calls(self) -> None:
        """While cover are moving, perform periodically update calls."""
        while self.is_moving():
            await asyncio.sleep(1)
            await self.after_update()
        if self._update_task:
            self._update_task.cancel()
            self._update_task = None

    async def set_position(
        self,
        position: Position,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
    ) -> None:
        """Set opening device to desired position.

        Parameters:
            * position: Position object containing the target position.
            * velocity: Velocity to be used during transition.
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        kwargs: Any = {}

        if (
            velocity is None or velocity is Velocity.DEFAULT
        ) and self.use_default_velocity:
            velocity = self.default_velocity

        if isinstance(velocity, Velocity):
            if velocity is not Velocity.DEFAULT:
                if velocity is Velocity.SILENT:
                    kwargs["fp1"] = Parameter(raw=b"\x00\x00")
                else:
                    kwargs["fp1"] = Parameter(raw=b"\xC8\x00")
        elif isinstance(velocity, int):
            kwargs["fp1"] = Position.from_percent(velocity)

        command = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=position,
            **kwargs,
        )
        await command.send()
        await self.after_update()

    async def open(
        self,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
    ) -> None:
        """Open opening device.

        Parameters:
            * velocity: Velocity to be used during transition.
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=self.open_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
        )

    async def close(
        self,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
    ) -> None:
        """Close opening device.

        Parameters:
            * velocity: Velocity to be used during transition.
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=self.close_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
        )

    async def stop(self, wait_for_completion: bool = True) -> None:
        """Stop opening device.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=CurrentPosition(), wait_for_completion=wait_for_completion
        )

    async def set_position_limitations(self,
                                       position_min: Position = IgnorePosition(),
                                       position_max: Position = IgnorePosition()) -> None:
        """Set a minimum and maximum position limit.

        Parameters:
            * min_position: Position object containing the minimum position.
            * max_position: Position object containing the maximum position.
        """
        command_set_limitation = SetLimitation(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            limitation_value_min=position_min,
            limitation_value_max=position_max
        )
        await command_set_limitation.do_api_call()
        if not command_set_limitation.success:
            raise PyVLXException("Unable to set limitations")
        self.limitation_min = position_min
        self.limitation_max = position_max
        await self.after_update()

    async def clear_position_limitations(self) -> None:
        """Clear position limits.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        command_set_limitation = SetLimitation(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            limitation_time=LimitationTimeClearAll(),
        )
        await command_set_limitation.do_api_call()
        if not command_set_limitation.success:
            raise PyVLXException("Unable to clear limitations")
        self.limitation_min = IgnorePosition()
        self.limitation_max = IgnorePosition()
        await self.after_update()

    async def get_limitation_min(self) -> Position:
        """Request and return minimum limitation from gateway."""
        command_get_limitation = GetLimitation(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            limitation_type=LimitationType.MIN_LIMITATION
        )
        await command_get_limitation.do_api_call()
        if not command_get_limitation.success:
            raise PyVLXException("Unable to get minimum limitation")

        self.limitation_min = Position(position_percent=command_get_limitation.min_value)

        return self.limitation_min

    async def get_limitation_max(self) -> Position:
        """Request and return maximum limitation from gateway."""
        command_get_limitation = GetLimitation(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            limitation_type=LimitationType.MAX_LIMITATION
        )
        await command_get_limitation.do_api_call()
        if not command_get_limitation.success:
            raise PyVLXException("Unable to get maximum limitation")

        self.limitation_max = Position(position_percent=command_get_limitation.max_value)

        return self.limitation_max

    def is_moving(self) -> bool:
        """Return moving state of the cover."""
        return self.is_opening or self.is_closing

    def movement_percent(self) -> int:
        """Return movement percentage of the cover."""
        if (
            self.estimated_completion is None
            or self.state_received_at is None
            or self.estimated_completion < datetime.datetime.now()
        ):
            return 100

        movement_duration_s: float = (
            self.estimated_completion - self.state_received_at
        ).total_seconds()
        time_passed_s: float = (
            datetime.datetime.now() - self.state_received_at
        ).total_seconds()

        percent: int = int(time_passed_s / movement_duration_s * 100)
        percent = max(percent, 0)
        percent = min(percent, 100)
        return percent

    def get_position(self) -> Position:
        """Return position of the cover."""
        if self.is_moving():
            percent = self.movement_percent()
            movement_origin = self.position.position_percent
            movement_target = self.target.position_percent
            current_position = (
                movement_origin + (movement_target - movement_origin) / 100 * percent
            )
            if not self._update_task:
                self._update_task = self.pyvlx.loop.create_task(self._update_calls())
            return Position(position_percent=int(current_position))
        return self.position

    def __str__(self) -> str:
        """Return object as readable string."""
        return '<{} name="{}" node_id="{}" serial_number="{}" position="{}"/>'.format(
            type(self).__name__,
            self.name,
            self.node_id,
            self.serial_number,
            self.position,
        )


class Window(OpeningDevice):
    """Window object."""

    def __init__(
        self,
        pyvlx: "PyVLX",
        node_id: int,
        name: str,
        serial_number: Optional[str],
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
        return '<{} name="{}" node_id="{}" rain_sensor={} serial_number="{}" position="{}"/>'.format(
            type(self).__name__,
            self.name,
            self.node_id,
            self.rain_sensor,
            self.serial_number,
            self.position,
        )

    @deprecated("Use 'get_limitation_min' instead.")
    async def get_limitation(self) -> GetLimitation:
        """Request minimum limitation and return it as part of the GetLimitation object."""
        get_limitation = GetLimitation(pyvlx=self.pyvlx, node_id=self.node_id)
        await get_limitation.do_api_call()
        if not get_limitation.success:
            raise PyVLXException("Unable to send command")
        return get_limitation


class Blind(OpeningDevice):
    """Blind objects."""

    def __init__(
        self,
        pyvlx: "PyVLX",
        node_id: int,
        name: str,
        serial_number: Optional[str],
        position_parameter: Parameter = Parameter(),
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
        self.orientation: Position = Position(position_percent=0)
        self.target_orientation: Position = TargetPosition()
        self.target_position: Position = TargetPosition()
        self.open_orientation_target: int = 50
        self.close_orientation_target: int = 100

    async def set_position_and_orientation(
        self,
        position: Position,
        wait_for_completion: bool = True,
        velocity: Velocity | int | None = None,
        orientation: Optional[Position] = None,
    ) -> None:
        """Set window to desired position.

        Parameters:
            * position: Position object containing the current position.
            * velocity: Velocity to be used during transition.
            * target_position: Position object holding the target position
                which allows to adjust the position while the blind is in movement
                without stopping the blind (if orientation position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.
            * orientation: If set, the orientation of the device will be set in the same request.
                Note, that, if the position is set to 0, the orientation will be set to 0 too.

        """
        self.target_position = position
        kwargs: Any = {}

        if orientation is not None:
            kwargs["fp3"] = orientation
        elif self.target_position == Position(position_percent=0):
            kwargs["fp3"] = Position(position_percent=0)
        else:
            kwargs["fp3"] = IgnorePosition()

        if (
            velocity is None or velocity is Velocity.DEFAULT
        ) and self.use_default_velocity:
            velocity = self.default_velocity

        if isinstance(velocity, Velocity):
            if velocity is not Velocity.DEFAULT:
                if velocity is Velocity.SILENT:
                    # The above code is declaring a variable called `kwargs`.
                    kwargs["fp1"] = Parameter(raw=b"\x00\x00")
                else:
                    kwargs["fp1"] = Parameter(raw=b"\xC8\x00")
        elif isinstance(velocity, int):
            kwargs["fp1"] = Position.from_percent(velocity)

        command = CommandSend(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            parameter=position,
            wait_for_completion=wait_for_completion,
            **kwargs
        )
        await command.send()
        await self.after_update()

    async def set_position(
        self,
        position: Position,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
    ) -> None:
        """Set window to desired position.

        Parameters:
            * position: Position object containing the current position.
            * velocity: Velocity to be used during transition.
            * target_position: Position object holding the target position
                which allows to adjust the position while the blind is in movement
                without stopping the blind (if orientation position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position_and_orientation(
            position=position,
            wait_for_completion=wait_for_completion,
            velocity=velocity,
        )

    async def open(
        self,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
    ) -> None:
        """Open window.

        Parameters:
            * velocity: Velocity to be used during transition.
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position(
            position=Position(position_percent=self.open_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
        )

    async def close(
        self,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
    ) -> None:
        """Close window.

        Parameters:
            * velocity: Velocity to be used during transition.
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position(
            position=Position(position_percent=self.close_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
        )

    async def stop(self, wait_for_completion: bool = True) -> None:
        """Stop Blind position."""
        await self.set_position_and_orientation(
            position=CurrentPosition(),
            wait_for_completion=wait_for_completion,
            orientation=self.target_orientation,
        )

    async def set_orientation(
        self, orientation: Position, wait_for_completion: bool = True
    ) -> None:
        """Set Blind shades to desired orientation.

        Parameters:
            * orientation: Position object containing the target orientation.
            + target_orientation: Position object holding the target orientation
                which allows to adjust the orientation while the blind is in movement
                without stopping the blind (if the position has been changed.)
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        self.target_orientation = orientation
        self.orientation = orientation

        fp3 = (
            Position(position_percent=0)
            if self.target_position == Position(position_percent=0)
            else self.target_orientation
        )

        print("Orientation in device: %s " % (orientation))
        command = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=self.target_position,
            fp3=fp3,
        )
        await command.send()
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


class DualRollerShutter(OpeningDevice):
    """DualRollerShutter object."""

    def __init__(
        self,
        pyvlx: "PyVLX",
        node_id: int,
        name: str,
        serial_number: Optional[str],
        position_parameter: Parameter = Parameter(),
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
        self.position_upper_curtain: Position = Position(position_percent=0)
        self.position_lower_curtain: Position = Position(position_percent=0)
        self.target_position: Any = Position()
        self.active_parameter: int = 0

    async def set_position(
        self,
        position: Position,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
        curtain: str = "dual",
    ) -> None:
        """Set DualRollerShutter to desired position.

        Parameters:
            * position: Position object containing the current position.
            * target_position: Position object holding the target position
                which allows to adjust the position while the blind is in movement
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        kwargs: Any = {}

        if curtain == "upper":
            self.target_position = DualRollerShutterPosition()
            self.active_parameter = 1
            kwargs["fp1"] = position
            kwargs["fp2"] = TargetPosition()
        elif curtain == "lower":
            self.target_position = DualRollerShutterPosition()
            self.active_parameter = 2
            kwargs["fp1"] = TargetPosition()
            kwargs["fp2"] = position
        else:
            self.target_position = position
            self.active_parameter = 0

        if (
            velocity is None or velocity is Velocity.DEFAULT
        ) and self.use_default_velocity:
            velocity = self.default_velocity

        if isinstance(velocity, Velocity):
            if velocity is not Velocity.DEFAULT:
                if velocity is Velocity.SILENT:
                    kwargs["fp3"] = Parameter(raw=b"\x00\x00")
                else:
                    kwargs["fp3"] = Parameter(raw=b"\xC8\x00")
        elif isinstance(velocity, int):
            kwargs["fp3"] = Position.from_percent(velocity)

        command = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=self.target_position,
            active_parameter=self.active_parameter,
            **kwargs
        )
        await command.send()
        if position.position <= Position.MAX:
            if curtain == "upper":
                self.position_upper_curtain = position
            elif curtain == "lower":
                self.position_lower_curtain = position
            else:
                self.position = position
        await self.after_update()

    async def open(
        self,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
        curtain: str = "dual",
    ) -> None:
        """Open DualRollerShutter.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        await self.set_position(
            position=Position(position_percent=self.open_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
            curtain=curtain,
        )

    async def close(
        self,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        wait_for_completion: bool = True,
        curtain: str = "dual",
    ) -> None:
        """Close DualRollerShutter.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.
        """
        await self.set_position(
            position=Position(position_percent=self.close_position_target),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
            curtain=curtain,
        )

    async def stop(
        self,
        wait_for_completion: bool = True,
        velocity: Velocity | int | None = Velocity.DEFAULT,
        curtain: str = "dual",
    ) -> None:
        """Stop Blind position."""
        await self.set_position(
            position=CurrentPosition(),
            velocity=velocity,
            wait_for_completion=wait_for_completion,
            curtain=curtain,
        )


class RollerShutter(OpeningDevice):
    """RollerShutter object."""


class GarageDoor(OpeningDevice):
    """GarageDoor object."""


class Gate(OpeningDevice):
    """Gate object."""


class Blade(OpeningDevice):
    """Blade object."""
