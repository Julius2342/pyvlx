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
        if frame.node_id not in self.pyvlx.nodes:
            return
        node = self.pyvlx.nodes[frame.node_id]

        status_reply_changed = node.last_frame_status_reply != frame.status_reply
        run_status_changed = node.last_frame_run_status != frame.run_status

        if status_reply_changed:
            node.last_frame_status_reply = frame.status_reply
        if run_status_changed:
            node.last_frame_run_status = frame.run_status

        something_changed = status_reply_changed or run_status_changed

        if isinstance(node, Blind):
            if (
                # MP and FP3 are needed in frame, so check if they are present before accessing them
                NodeParameter(0) in frame.parameter_data  # MP
                and NodeParameter(3) in frame.parameter_data  # FP3
            ):
                position = Position(frame.parameter_data[NodeParameter(0)])
                orientation = Position(frame.parameter_data[NodeParameter(3)])
                if position.position <= Parameter.MAX and node.position != position:
                    node.position = position
                    PYVLXLOG.debug("%s position changed to: %s", node.name, position)
                    something_changed = True
                if orientation.position <= Parameter.MAX and node.orientation != orientation:
                    node.orientation = orientation
                    PYVLXLOG.debug("%s orientation changed to: %s", node.name, orientation)
                    something_changed = True

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
                if position.position <= Parameter.MAX and node.position != position:
                    node.position = position
                    PYVLXLOG.debug("%s position changed to: %s", node.name, position)
                    something_changed = True
                if (
                    position_upper_curtain.position <= Parameter.MAX
                    and node.position_upper_curtain != position_upper_curtain
                ):
                    node.position_upper_curtain = position_upper_curtain
                    PYVLXLOG.debug(
                        "%s position upper curtain changed to: %s",
                        node.name,
                        position_upper_curtain,
                    )
                    something_changed = True
                if (
                    position_lower_curtain.position <= Parameter.MAX
                    and node.position_lower_curtain != position_lower_curtain
                ):
                    node.position_lower_curtain = position_lower_curtain
                    PYVLXLOG.debug(
                        "%s position lower curtain changed to: %s",
                        node.name,
                        position_lower_curtain,
                    )
                    something_changed = True

        if something_changed:
            await node.after_update()

    def _update_opening_device_status(
        self,
        node: OpeningDevice,
        frame: Union[
            FrameGetAllNodesInformationNotification,
            FrameNodeStatePositionChangedNotification,
        ],
        position: Position,
        target: Position,
    ) -> None:
        if (position.position <= Parameter.MAX and position.position > target.position and target.position <= Parameter.MAX) and (
            (frame.state == OperatingState.EXECUTING)
            or frame.remaining_time > 0
        ):
            node.is_opening = True
            node.is_closing = False
            PYVLXLOG.debug("%s is opening", node.name)
            node.state_received_at = datetime.datetime.now()
            node.estimated_completion = (
                node.state_received_at
                + datetime.timedelta(0, frame.remaining_time)
            )
            PYVLXLOG.debug(
                "%s will be opening until %s", node.name, node.estimated_completion
            )
            return

        if (position.position <= Parameter.MAX and position.position < target.position and target.position <= Parameter.MAX) and (
            (frame.state == OperatingState.EXECUTING)
            or frame.remaining_time > 0
        ):
            node.is_closing = True
            node.is_opening = False
            PYVLXLOG.debug("%s is closing", node.name)
            node.state_received_at = datetime.datetime.now()
            node.estimated_completion = (
                node.state_received_at
                + datetime.timedelta(0, frame.remaining_time)
            )
            PYVLXLOG.debug(
                "%s will be closing until %s", node.name, node.estimated_completion
            )
            return

        if node.is_opening:
            node.is_opening = False
            node.state_received_at = None
            node.estimated_completion = None
            PYVLXLOG.debug("%s stops opening", node.name)
        if node.is_closing:
            node.is_closing = False
            PYVLXLOG.debug("%s stops closing", node.name)

    async def _update_node_main_parameter(
        self,
        node: Any,
        frame: Union[
            FrameGetAllNodesInformationNotification,
            FrameNodeStatePositionChangedNotification,
        ],
        position: Position,
        target: Position,
    ) -> None:
        if isinstance(node, OpeningDevice):
            if position.position <= Parameter.MAX:
                node.position = position
                node.target = target
                PYVLXLOG.debug(
                    "%s position changed to: %s",
                    node.name,
                    position,
                )
            await node.after_update()
            return

        if isinstance(node, DimmableDevice):
            intensity = Intensity(frame.current_position)
            if intensity.intensity <= Parameter.MAX:
                node.intensity = intensity
                PYVLXLOG.debug(
                    "%s intensity changed to: %s",
                    node.name,
                    intensity,
                )
            await node.after_update()
            return

        if isinstance(node, OnOffSwitch):
            state = SwitchParameter(frame.current_position)
            switch_target = SwitchParameter(frame.target)
            if state.state == switch_target.state:
                if state.state == Parameter.ON:
                    node.parameter = state
                    PYVLXLOG.debug(
                        "%s state changed to: %s",
                        node.name,
                        state,
                    )
                elif state.state == Parameter.OFF:
                    node.parameter = state
                    PYVLXLOG.debug(
                        "%s state changed to: %s",
                        node.name,
                        state,
                    )
                await node.after_update()

    async def _process_node_state_frame(
        self,
        frame: Union[
            FrameGetAllNodesInformationNotification,
            FrameNodeStatePositionChangedNotification,
        ],
    ) -> None:
        PYVLXLOG.debug("NodeUpdater process frame: %s", frame)
        if frame.node_id not in self.pyvlx.nodes:
            return

        node = self.pyvlx.nodes[frame.node_id]
        node.last_frame_state = frame.state

        position = Position(frame.current_position)
        target = Position(frame.target)
        if isinstance(node, OpeningDevice):
            self._update_opening_device_status(node, frame, position, target)

        await self._update_node_main_parameter(node, frame, position, target)

    async def _process_command_run_status_notification(
        self,
        frame: FrameCommandRunStatusNotification,
    ) -> None:
        node_id = frame.index_id
        if node_id is None:
            return
        if node_id not in self.pyvlx.nodes:
            return

        node = self.pyvlx.nodes[node_id]
        node.last_frame_run_status = frame.run_status
        node.last_frame_status_reply = frame.status_reply
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
            await self._process_node_state_frame(frame)
        elif isinstance(frame, FrameStatusRequestNotification):
            await self.process_frame_status_request_notification(frame)
        elif isinstance(frame, FrameCommandRunStatusNotification):
            await self._process_command_run_status_notification(frame)
