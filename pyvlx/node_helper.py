"""Helper module for Node objects."""
from typing import TYPE_CHECKING, Optional, Union

from .api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameGetNodeInformationNotification)
from .const import NodeTypeWithSubtype
from .lightening_device import Light
from .log import PYVLXLOG
from .node import Node
from .on_off_switch import OnOffSwitch
from .opening_device import (
    Awning, Blade, Blind, DualRollerShutter, GarageDoor, Gate, RollerShutter,
    Window)

if TYPE_CHECKING:
    from pyvlx import PyVLX


def convert_frame_to_node(
    pyvlx: "PyVLX",
    frame: Union[
        FrameGetNodeInformationNotification, FrameGetAllNodesInformationNotification
    ],
) -> Optional[Node]:
    """Convert FrameGet[All]Node[s]InformationNotification into Node object."""
    # pylint: disable=too-many-return-statements

    if frame.node_type == NodeTypeWithSubtype.WINDOW_OPENER:
        return Window(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
            rain_sensor=False,
        )

    if frame.node_type == NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR:
        return Window(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
            rain_sensor=True,
        )

    if frame.node_type == NodeTypeWithSubtype.DUAL_ROLLER_SHUTTER:
        return DualRollerShutter(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type in [
        NodeTypeWithSubtype.ROLLER_SHUTTER,
        NodeTypeWithSubtype.SWINGING_SHUTTERS,
    ]:
        return RollerShutter(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type in [
        NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND,
        NodeTypeWithSubtype.VERTICAL_INTERIOR_BLINDS,
        NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND,
    ]:
        return RollerShutter(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
        )

    # Blinds have position and orientation (inherit frame.current_position_fp3) attribute
    if frame.node_type in [
        NodeTypeWithSubtype.EXTERIOR_VENETIAN_BLIND,
        NodeTypeWithSubtype.ADJUSTABLE_SLUTS_ROLLING_SHUTTER,
        NodeTypeWithSubtype.LOUVER_BLIND,
    ]:
        return Blind(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type in [
        NodeTypeWithSubtype.VERTICAL_EXTERIOR_AWNING,
        NodeTypeWithSubtype.HORIZONTAL_AWNING,
    ]:
        return Awning(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type == NodeTypeWithSubtype.ON_OFF_SWITCH:
        return OnOffSwitch(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
        )

    if frame.node_type in [
        NodeTypeWithSubtype.GARAGE_DOOR_OPENER,
        NodeTypeWithSubtype.LINAR_ANGULAR_POSITION_OF_GARAGE_DOOR,
    ]:
        return GarageDoor(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type == NodeTypeWithSubtype.GATE_OPENER:
        return Gate(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type == NodeTypeWithSubtype.GATE_OPENER_ANGULAR_POSITION:
        return Gate(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type == NodeTypeWithSubtype.BLADE_OPENER:
        return Blade(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
            position_parameter=frame.current_position,
        )

    if frame.node_type in [NodeTypeWithSubtype.LIGHT, NodeTypeWithSubtype.LIGHT_ON_OFF]:
        return Light(
            pyvlx=pyvlx,
            node_id=frame.node_id,
            name=frame.name,
            serial_number=frame.serial_number,
        )

    PYVLXLOG.warning("%s not implemented", frame.node_type)
    return None
