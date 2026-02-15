"""Helper module for Node objects."""
from math import floor
from typing import TYPE_CHECKING, Optional, Union

from .api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameGetNodeInformationNotification)
from .const import NodeType, NodeTypeWithSubtype
from .dimmable_device import ExteriorHeating, Light, OnOffLight
from .log import PYVLXLOG
from .node import Node
from .on_off_switch import OnOffSwitch
from .opening_device import (
    Awning, Blade, Blind, DualRollerShutter, GarageDoor, Gate, RollerShutter,
    Window)

if TYPE_CHECKING:
    from pyvlx import PyVLX


def convert_frame_to_node(pyvlx: "PyVLX",
                          frame: Union[FrameGetNodeInformationNotification, FrameGetAllNodesInformationNotification]) -> Optional[Node]:
    """Convert FrameGet[All]Node[s]InformationNotification into Node object."""
    # pylint: disable=too-many-return-statements

    match NodeType(floor(frame.node_type.value / 64)):
        case NodeType.VENETIAN_BLIND | NodeType.BLIND:  # 1, 10
            # this seems wrong : VENITIAN_BLIND excepts FP1, FP2 and FP3
            return RollerShutter(pyvlx, frame.node_id, frame.name, frame.serial_number)

        case NodeType.ROLLER_SHUTTER:  # 2
            if frame.node_type == NodeTypeWithSubtype.ADJUSTABLE_SLATS_ROLLING_SHUTTER:
                return Blind(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)
            return RollerShutter(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

        case NodeType.AWNING | NodeType.HORIZONTAL_AWNING:  # 3, 16
            return Awning(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

        case NodeType.WINDOW_OPENER:  # 4
            return Window(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position,
                          (frame.node_type == NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR))

        case NodeType.GARAGE_OPENER:  # 5
            return GarageDoor(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

        case NodeType.LIGHT:  # 6
            if frame.node_type == NodeTypeWithSubtype.LIGHT_ON_OFF :
                return OnOffLight(pyvlx, frame.node_id, frame.name, frame.serial_number)
            return Light(pyvlx, frame.node_id, frame.name, frame.serial_number)

        case NodeType.GATE_OPENER:  # 7
            return Gate(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

        case NodeType.DUAL_SHUTTER:  # 13
            return DualRollerShutter(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

        case NodeType.EXTERNAL_VENETIAN_BLIND | NodeType.LOUVRE_BLIND:  # 17, 18
            return Blind(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

        case NodeType.ON_OFF_SWITCH:  # 15
            return OnOffSwitch(pyvlx, frame.node_id, frame.name, frame.serial_number)

        case NodeType.EXTERIOR_HEATING:  # 21
            return ExteriorHeating(pyvlx, frame.node_id, frame.name, frame.serial_number)

        case NodeType.BLADE_OPENER:  # 29
            return Blade(pyvlx, frame.node_id, frame.name, frame.serial_number, frame.current_position)

    PYVLXLOG.warning("%s not implemented", frame.node_type)
    return None
