"""Module for updating nodes via frames."""
import datetime
from typing import TYPE_CHECKING, Any, Union

from .api.frames import (
    FrameBase, FrameCommandRunStatusNotification,
    FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification, FrameStatusRequestNotification)
from .const import NodeParameter, OperatingState
from .dimmable_device import DimmableDevice
from .log import PYVLXLOG
from .node import Node
from .on_off_switch import OnOffSwitch
from .opening_device import Blind, DualRollerShutter, OpeningDevice
from .parameter import Intensity, Parameter, Position, SwitchParameter

if TYPE_CHECKING:
    from pyvlx import PyVLX


def _set_node_property(node: Node, prop_name: str, new_value: Any, log_unchanged: bool = False) -> bool:
    """Update a node property if changed, logging the result.

    Returns True if the property was actually changed.
    """
    current_value = getattr(node, prop_name)
    if current_value != new_value:
        setattr(node, prop_name, new_value)
        PYVLXLOG.debug("%s %s changed to: %s", node.name, prop_name, new_value)
        return True
    if log_unchanged:
        PYVLXLOG.debug("%s %s unchanged: %s", node.name, prop_name, new_value)
    return False


class NodeUpdater:
    """Class for updating nodes via incoming frames,  usually received by house monitor."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize NodeUpdater object."""
        self.pyvlx = pyvlx

    async def process_frame_status_request_notification(
        self, frame: FrameStatusRequestNotification
    ) -> None:
        """Process FrameStatusRequestNotification."""
        if frame.node_id not in self.pyvlx.nodes:
            PYVLXLOG.warning("NodeUpdater: Received status request notification for unknown node_id %s", frame.node_id)
            return
        node = self.pyvlx.nodes[frame.node_id]

        node_changed = False
        node_changed |= _set_node_property(node, "last_frame_status_reply", new_value=frame.status_reply)
        node_changed |= _set_node_property(node, "last_frame_run_status", new_value=frame.run_status)

        if isinstance(node, Blind):
            if (
                # MP and FP3 are needed in frame, so check if they are present before accessing them
                NodeParameter(0) in frame.parameter_data  # MP
                and NodeParameter(3) in frame.parameter_data  # FP3
            ):
                position = Position(frame.parameter_data[NodeParameter(0)])
                orientation = Position(frame.parameter_data[NodeParameter(3)])
                if position.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "position", position)
                if orientation.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "orientation", orientation)

        elif isinstance(node, DualRollerShutter):
            if (
                # MP, FP1 and FP2 are needed in frame,
                # so check if they are present before accessing them
                NodeParameter(0) in frame.parameter_data  # MP
                and NodeParameter(1) in frame.parameter_data  # FP1
                and NodeParameter(2) in frame.parameter_data  # FP2
            ):
                position = Position(frame.parameter_data[NodeParameter(0)])
                position_upper_curtain = Position(frame.parameter_data[NodeParameter(1)])
                position_lower_curtain = Position(frame.parameter_data[NodeParameter(2)])
                if position.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "position", position)
                if position_upper_curtain.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "position_upper_curtain", position_upper_curtain)
                if position_lower_curtain.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "position_lower_curtain", position_lower_curtain)

        if node_changed:
            await node.after_update()

    async def _update_opening_device_status(
        self,
        node: OpeningDevice,
        frame: Union[
            FrameGetAllNodesInformationNotification,
            FrameNodeStatePositionChangedNotification,
        ]
    ) -> bool:

        position = Position(frame.current_position)
        target = Position(frame.target)

        node_changed = False

        if (position.position <= Parameter.MAX and position.position > target.position and target.position <= Parameter.MAX) and (
            (frame.state == OperatingState.EXECUTING)
            or frame.remaining_time > 0
        ):
            node_changed |= _set_node_property(node, "is_opening", True)
            node_changed |= _set_node_property(node, "is_closing", False)
            node.state_received_at = datetime.datetime.now()
            node.estimated_completion = (
                node.state_received_at
                + datetime.timedelta(0, frame.remaining_time)
            )
            PYVLXLOG.debug(
                "%s is opening (%s->%s), estimated completion in %ss at %s",
                node.name, position, target,
                frame.remaining_time,
                node.estimated_completion.strftime("%Y-%m-%d %H:%M:%S")
            )

        elif (position.position < target.position <= Parameter.MAX) and (
            (frame.state == OperatingState.EXECUTING)
            or frame.remaining_time > 0
        ):
            node_changed |= _set_node_property(node, "is_closing", True)
            node_changed |= _set_node_property(node, "is_opening", False)
            node.state_received_at = datetime.datetime.now()
            node.estimated_completion = (
                node.state_received_at
                + datetime.timedelta(0, frame.remaining_time)
            )
            PYVLXLOG.debug(
                "%s is closing (%s->%s), estimated completion in %ss at %s",
                node.name, position, target,
                frame.remaining_time,
                node.estimated_completion.strftime("%Y-%m-%d %H:%M:%S")
            )

        else:
            if node.is_opening:
                node_changed |= _set_node_property(node, "is_opening", False)
                node.state_received_at = None
                node.estimated_completion = None
                PYVLXLOG.debug("%s stopped opening", node.name)
            if node.is_closing:
                node_changed |= _set_node_property(node, "is_closing", False)
                node.state_received_at = None
                node.estimated_completion = None
                PYVLXLOG.debug("%s stopped closing", node.name)
        return node_changed

    async def _update_node_main_parameter(
        self,
        node: Any,
        frame: Union[
            FrameGetAllNodesInformationNotification,
            FrameNodeStatePositionChangedNotification,
        ]
    ) -> bool:

        node_changed = False
        if isinstance(node, OpeningDevice):
            position = Position(frame.current_position)
            target = Position(frame.target)
            if position.position <= Parameter.MAX:
                node_changed |= _set_node_property(node, "position", position)
                node_changed |= _set_node_property(node, "target", target)

        if isinstance(node, DimmableDevice):
            intensity = Intensity(frame.current_position)
            if intensity.intensity <= Parameter.MAX:
                node_changed |= _set_node_property(node, "intensity", intensity)

        if isinstance(node, OnOffSwitch):
            state = SwitchParameter(frame.current_position)
            switch_target = SwitchParameter(frame.target)
            if (state.state == switch_target.state
               and state.state in (Parameter.ON, Parameter.OFF)):
                node_changed |= _set_node_property(node, "parameter", state)

        return node_changed

    async def _process_node_state_frame(
        self,
        frame: Union[
            FrameGetAllNodesInformationNotification,
            FrameNodeStatePositionChangedNotification,
        ],
    ) -> None:
        if frame.node_id not in self.pyvlx.nodes:
            PYVLXLOG.debug("NodeUpdater: Received state frame for unknown node_id %s", frame.node_id)
            return

        node = self.pyvlx.nodes[frame.node_id]

        node_changed = False
        node_changed |= _set_node_property(node, "last_frame_state", new_value=frame.state)

        if isinstance(node, OpeningDevice):
            node_changed |= await self._update_opening_device_status(node, frame)
        node_changed |= await self._update_node_main_parameter(node, frame)

        if node_changed:
            await node.after_update()

    async def _process_command_run_status_notification(
        self,
        frame: FrameCommandRunStatusNotification,
    ) -> None:
        if frame.index_id is None or frame.index_id not in self.pyvlx.nodes:
            PYVLXLOG.warning("NodeUpdater: Received FrameCommandRunStatusNotification for unknown index_id %s", frame.index_id)
            return
        node = self.pyvlx.nodes[frame.index_id]

        node_changed = False
        node_changed |= _set_node_property(node, "last_frame_status_reply", new_value=frame.status_reply)
        node_changed |= _set_node_property(node, "last_frame_run_status", new_value=frame.run_status)

        if node_changed:
            await node.after_update()

    async def process_frame(self, frame: FrameBase) -> None:
        """Update nodes via frame, usually received by house monitor."""
        PYVLXLOG.debug("NodeUpdater process frame: %s", frame.__class__.__name__)

        if isinstance(frame, (FrameGetAllNodesInformationNotification, FrameNodeStatePositionChangedNotification)):
            await self._process_node_state_frame(frame)
        elif isinstance(frame, FrameStatusRequestNotification):
            await self.process_frame_status_request_notification(frame)
        elif isinstance(frame, FrameCommandRunStatusNotification):
            await self._process_command_run_status_notification(frame)
