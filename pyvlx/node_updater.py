"""Module for updating nodes via frames."""
import datetime
from typing import TYPE_CHECKING, Any

from .api.frames import (
    FrameBase, FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification, FrameStatusRequestNotification)
from .const import NodeParameter, OperatingState
from .dimmable_device import DimmableDevice
from .log import PYVLXLOG
from .on_off_switch import OnOffSwitch
from .opening_device import Blind, DualRollerShutter, OpeningDevice
from .parameter import Intensity, Parameter, Position, SwitchParameter

if TYPE_CHECKING:
    from pyvlx import PyVLX


def _update_property(node: Any, prop_name: str, new_value: Any) -> bool:
    """Update a node property if changed, logging the result.

    Returns True if the property was actually changed.
    """
    current_value = getattr(node, prop_name)
    if current_value != new_value:
        setattr(node, prop_name, new_value)
        PYVLXLOG.debug("%s %s changed to: %s", node.name, prop_name, new_value)
        return True
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
        PYVLXLOG.debug("NodeUpdater process frame: %s", frame)
        if frame.node_id not in self.pyvlx.nodes:
            PYVLXLOG.warning("NodeUpdater: Received status request notification for unknown node_id %s", frame.node_id)
            return
        node = self.pyvlx.nodes[frame.node_id]
        changed = False

        changed |= _update_property(node, "last_frame_status_reply", frame.status_reply)

        if isinstance(node, Blind):
            if (
                # MP and FP3 are needed in frame, so check if they are present before accessing them
                NodeParameter(0) in frame.parameter_data  # MP
                and NodeParameter(3) in frame.parameter_data  # FP3
            ):
                position = Position(frame.parameter_data[NodeParameter(0)])
                orientation = Position(frame.parameter_data[NodeParameter(3)])
                if position.position <= Parameter.MAX:
                    changed |= _update_property(node, "position", position)
                if orientation.position <= Parameter.MAX:
                    changed |= _update_property(node, "orientation", orientation)

        elif isinstance(node, DualRollerShutter):
            if (
                # MP, FP1 and FP2 are needed in frame, so check if they are present before accessing them
                NodeParameter(0) in frame.parameter_data  # MP
                and NodeParameter(1) in frame.parameter_data  # FP1
                and NodeParameter(2) in frame.parameter_data  # FP2
            ):
                position = Position(frame.parameter_data[NodeParameter(0)])
                position_upper_curtain = Position(frame.parameter_data[NodeParameter(1)])
                position_lower_curtain = Position(frame.parameter_data[NodeParameter(2)])
                if position.position <= Parameter.MAX:
                    changed |= _update_property(node, "position", position)
                if position_upper_curtain.position <= Parameter.MAX:
                    changed |= _update_property(node, "position_upper_curtain", position_upper_curtain)
                if position_lower_curtain.position <= Parameter.MAX:
                    changed |= _update_property(node, "position_lower_curtain", position_lower_curtain)

        if changed:
            await node.after_update()

    async def process_frame(self, frame: FrameBase) -> None:
        """Update nodes via frame, usually received by house monitor."""
        if isinstance(
            frame,
            (
                FrameGetAllNodesInformationNotification,
                FrameNodeStatePositionChangedNotification,
            ),
        ):
            PYVLXLOG.debug("NodeUpdater process frame: %s", frame)
            if frame.node_id not in self.pyvlx.nodes:
                PYVLXLOG.warning("NodeUpdater: Received frame for unknown node_id %s", frame.node_id)
                return
            node = self.pyvlx.nodes[frame.node_id]
            changed = False

            # Set last_frame_state from frame
            changed |= _update_property(node, "last_frame_state", frame.state)

            position = Position(frame.current_position)
            target: Any = Position(frame.target)
            # KLF transmits for functional parameters basically always 'No feed-back value known’ (0xF7FF).
            # In home assistant this cause unreasonable values like -23%. Therefore a check is implemented
            # whether the frame parameter is inside the maximum range.

            # Set opening device status
            if isinstance(node, OpeningDevice):
                if (position.position > target.position <= Parameter.MAX) and (
                    (frame.state == OperatingState.EXECUTING)
                    or frame.remaining_time > 0
                ):
                    node.is_opening = True
                    PYVLXLOG.debug("%s is opening", node.name)
                    node.state_received_at = datetime.datetime.now()
                    node.estimated_completion = (
                        node.state_received_at
                        + datetime.timedelta(0, frame.remaining_time)
                    )
                    PYVLXLOG.debug(
                        "%s will be opening until", node.estimated_completion
                    )
                elif (position.position < target.position <= Parameter.MAX) and (
                    (frame.state == OperatingState.EXECUTING)
                    or frame.remaining_time > 0
                ):
                    node.is_closing = True
                    PYVLXLOG.debug("%s is closing", node.name)
                    node.state_received_at = datetime.datetime.now()
                    node.estimated_completion = (
                        node.state_received_at
                        + datetime.timedelta(0, frame.remaining_time)
                    )
                    PYVLXLOG.debug(
                        "%s will be closing until", node.estimated_completion
                    )
                else:
                    if node.is_opening:
                        node.is_opening = False
                        node.state_received_at = None
                        node.estimated_completion = None
                        PYVLXLOG.debug("%s stops opening", node.name)
                    if node.is_closing:
                        node.is_closing = False
                        PYVLXLOG.debug("%s stops closing", node.name)

            # Set main parameter
            if isinstance(node, OpeningDevice):
                if position.position <= Parameter.MAX:
                    changed |= _update_property(node, "position", position)
                    changed |= _update_property(node, "target", target)
            elif isinstance(node, DimmableDevice):
                intensity = Intensity(frame.current_position)
                if intensity.intensity <= Parameter.MAX:
                    changed |= _update_property(node, "intensity", intensity)
            elif isinstance(node, OnOffSwitch):
                state = SwitchParameter(frame.current_position)
                target = SwitchParameter(frame.target)
                if state.state == target.state:
                    if state.state in (Parameter.ON, Parameter.OFF):
                        changed |= _update_property(node, "parameter", state)

            if changed:
                await node.after_update()
        elif isinstance(frame, FrameStatusRequestNotification):
            await self.process_frame_status_request_notification(frame)
