"""Module for updating nodes via frames."""
import datetime
from typing import TYPE_CHECKING, Any

from .api.frames import (
    FrameBase, FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification, FrameStatusRequestNotification)
from .const import NodeParameter, OperatingState
from .lightening_device import LighteningDevice
from .log import PYVLXLOG
from .on_off_switch import OnOffSwitch
from .opening_device import Blind, DualRollerShutter, OpeningDevice
from .parameter import Intensity, Parameter, Position, SwitchParameter

if TYPE_CHECKING:
    from pyvlx import PyVLX


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
            return
        node = self.pyvlx.nodes[frame.node_id]
        if isinstance(node, Blind):
            if NodeParameter(0) not in frame.parameter_data:  # MP missing in frame
                return
            if NodeParameter(3) not in frame.parameter_data:  # FP3 missing in frame
                return
            position = Position(frame.parameter_data[NodeParameter(0)])
            orientation = Position(frame.parameter_data[NodeParameter(3)])
            if position.position <= Parameter.MAX:
                node.position = position
                PYVLXLOG.debug("%s position changed to: %s", node.name, position)
            if orientation.position <= Parameter.MAX:
                node.orientation = orientation
                PYVLXLOG.debug("%s orientation changed to: %s", node.name, orientation)
            await node.after_update()

        if isinstance(node, DualRollerShutter):
            if NodeParameter(0) not in frame.parameter_data:  # MP missing in frame
                return
            if NodeParameter(1) not in frame.parameter_data:  # FP1 missing in frame
                return
            if NodeParameter(2) not in frame.parameter_data:  # FP2 missing in frame
                return
            position = Position(frame.parameter_data[NodeParameter(0)])
            position_upper_curtain = Position(frame.parameter_data[NodeParameter(1)])
            position_lower_curtain = Position(frame.parameter_data[NodeParameter(2)])
            if position.position <= Parameter.MAX:
                node.position = position
                PYVLXLOG.debug("%s position changed to: %s", node.name, position)
            if position_upper_curtain.position <= Parameter.MAX:
                node.position_upper_curtain = position_upper_curtain
                PYVLXLOG.debug(
                    "%s position upper curtain changed to: %s",
                    node.name,
                    position_upper_curtain,
                )
            if position_lower_curtain.position <= Parameter.MAX:
                node.position_lower_curtain = position_lower_curtain
                PYVLXLOG.debug(
                    "%s position lower curtain changed to: %s",
                    node.name,
                    position_lower_curtain,
                )
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
                return
            node = self.pyvlx.nodes[frame.node_id]
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
                    node.position = position
                    node.target = target
                    PYVLXLOG.debug("%s position changed to: %s", node.name, position)
                await node.after_update()
            elif isinstance(node, LighteningDevice):
                intensity = Intensity(frame.current_position)
                if intensity.intensity <= Parameter.MAX:
                    node.intensity = intensity
                    PYVLXLOG.debug("%s intensity changed to: %s", node.name, intensity)
                await node.after_update()
            elif isinstance(node, OnOffSwitch):
                state = SwitchParameter(frame.current_position)
                target = SwitchParameter(frame.target)
                if state.state == target.state:
                    if state.state == Parameter.ON:
                        node.parameter = state
                        PYVLXLOG.debug("%s state changed to: %s", node.name, state)
                    elif state.state == Parameter.OFF:
                        node.parameter = state
                        PYVLXLOG.debug("%s state changed to: %s", node.name, state)
                    await node.after_update()
        elif isinstance(frame, FrameStatusRequestNotification):
            await self.process_frame_status_request_notification(frame)
