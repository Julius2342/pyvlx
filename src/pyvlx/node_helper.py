"""Helper module for Node objects."""
from typing import TYPE_CHECKING, Any, Callable

from .api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameGetNodeInformationNotification)
from .const import NodeTypeWithSubtype
from .dimmable_device import ExteriorHeating, Light, OnOffLight
from .log import PYVLXLOG
from .node import Node
from .on_off_switch import OnOffSwitch
from .opening_device import (
    Awning, Blade, Blind, DualRollerShutter, GarageDoor, Gate, RollerShutter,
    Window)

if TYPE_CHECKING:
    from pyvlx import PyVLX


FrameNodeInformation = (
    FrameGetNodeInformationNotification | FrameGetAllNodesInformationNotification
)
NodeFactory = Callable[["PyVLX", FrameNodeInformation], Node]


def _base_kwargs(
    pyvlx: "PyVLX", frame: FrameNodeInformation
) -> dict[str, Any]:
    """Return constructor kwargs shared by all node types."""
    return {
        "pyvlx": pyvlx,
        "node_id": frame.node_id,
        "name": frame.name,
        "serial_number": frame.serial_number,
    }


def _node_factory(
    node_constructor: Callable[..., Node],
    *,
    use_position: bool = True,
    rain_sensor: bool | None = None,
) -> NodeFactory:
    """Build a factory for node constructors with optional extras."""

    def _factory(pyvlx: "PyVLX", frame: FrameNodeInformation) -> Node:
        kwargs = _base_kwargs(pyvlx=pyvlx, frame=frame)
        if use_position:
            kwargs["position_parameter"] = frame.current_position
        if rain_sensor is not None:
            kwargs["rain_sensor"] = rain_sensor
        return node_constructor(**kwargs)

    return _factory


NODE_FACTORY: dict[NodeTypeWithSubtype, NodeFactory] = {
    NodeTypeWithSubtype.WINDOW_OPENER: _node_factory(Window, rain_sensor=False),
    NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR: _node_factory(Window, rain_sensor=True),
    NodeTypeWithSubtype.DUAL_ROLLER_SHUTTER: _node_factory(DualRollerShutter),
    NodeTypeWithSubtype.ROLLER_SHUTTER: _node_factory(RollerShutter),
    NodeTypeWithSubtype.SWINGING_SHUTTERS: _node_factory(RollerShutter),
    # Unclear why the next two do not have position, possibly just an oversight when introduced initially
    NodeTypeWithSubtype.VERTICAL_INTERIOR_BLINDS: _node_factory(RollerShutter, use_position=False),
    NodeTypeWithSubtype.INTERIOR_VENETIAN_BLIND: _node_factory(RollerShutter, use_position=False),
    NodeTypeWithSubtype.EXTERIOR_VENETIAN_BLIND: _node_factory(Blind),
    NodeTypeWithSubtype.ADJUSTABLE_SLATS_ROLLING_SHUTTER: _node_factory(Blind),
    NodeTypeWithSubtype.LOUVER_BLIND: _node_factory(Blind),
    NodeTypeWithSubtype.VERTICAL_EXTERIOR_AWNING: _node_factory(Awning),
    NodeTypeWithSubtype.HORIZONTAL_AWNING: _node_factory(Awning),
    NodeTypeWithSubtype.HORIZONTAL_AWNING_ALT: _node_factory(Awning),
    NodeTypeWithSubtype.GARAGE_DOOR_OPENER: _node_factory(GarageDoor),
    NodeTypeWithSubtype.LINEAR_ANGULAR_POSITION_OF_GARAGE_DOOR: _node_factory(GarageDoor),
    NodeTypeWithSubtype.GATE_OPENER: _node_factory(Gate),
    NodeTypeWithSubtype.GATE_OPENER_ANGULAR_POSITION: _node_factory(Gate),
    NodeTypeWithSubtype.BLADE_OPENER: _node_factory(Blade),
    NodeTypeWithSubtype.ON_OFF_SWITCH: _node_factory(OnOffSwitch, use_position=False),
    NodeTypeWithSubtype.LIGHT: _node_factory(Light, use_position=False),
    NodeTypeWithSubtype.LIGHT_ON_OFF: _node_factory(OnOffLight, use_position=False),
    NodeTypeWithSubtype.EXTERIOR_HEATING: _node_factory(ExteriorHeating, use_position=False),
}


def convert_frame_to_node(
    pyvlx: "PyVLX",
    frame: FrameNodeInformation,
) -> Node | None:
    """Convert FrameGet[All]Node[s]InformationNotification into Node object."""
    factory = NODE_FACTORY.get(frame.node_type)
    if factory is not None:
        return factory(pyvlx, frame)

    PYVLXLOG.warning("%s not implemented", frame.node_type)
    return None
