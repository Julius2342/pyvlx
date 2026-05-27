"""Module for updating nodes via frames."""
import datetime
from typing import TYPE_CHECKING, Any

from .api.frames import (
    FrameBase, FrameCommandRunStatusNotification,
    FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification, FrameStatusRequestNotification)
from .const import NodeParameter, OperatingState, RunStatus, StatusReply
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

    @staticmethod
    def _is_concrete_position(position: Position) -> bool:
        """Return True when a position can be used for movement comparisons."""
        return position.position <= Parameter.MAX

    @staticmethod
    def _clear_opening_device_motion(node: OpeningDevice) -> bool:
        """Clear stale motion state for a completed opening device movement."""
        node_changed = False
        node_changed |= _set_node_property(node, "is_opening", False)
        node_changed |= _set_node_property(node, "is_closing", False)
        node.state_received_at = None
        node.estimated_completion = None
        return node_changed

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

        status_position: Position | None = None
        status_position_is_concrete = False
        if NodeParameter(0) in frame.parameter_data:  # MP
            status_position = Position(frame.parameter_data[NodeParameter(0)])
            status_position_is_concrete = self._is_concrete_position(status_position)

        if isinstance(node, Blind):
            if (
                # MP and FP3 are needed in frame, so check if they are present before accessing them
                status_position is not None
                and NodeParameter(3) in frame.parameter_data  # FP3
            ):
                orientation = Position(frame.parameter_data[NodeParameter(3)])
                if status_position_is_concrete:
                    node_changed |= _set_node_property(node, "position", status_position)
                if orientation.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "orientation", orientation)

        elif isinstance(node, DualRollerShutter):
            if (
                # MP, FP1 and FP2 are needed in frame,
                # so check if they are present before accessing them
                status_position is not None
                and NodeParameter(1) in frame.parameter_data  # FP1
                and NodeParameter(2) in frame.parameter_data  # FP2
            ):
                position_upper_curtain = Position(frame.parameter_data[NodeParameter(1)])
                position_lower_curtain = Position(frame.parameter_data[NodeParameter(2)])
                if status_position_is_concrete:
                    node_changed |= _set_node_property(node, "position", status_position)
                if position_upper_curtain.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "position_upper_curtain", position_upper_curtain)
                if position_lower_curtain.position <= Parameter.MAX:
                    node_changed |= _set_node_property(node, "position_lower_curtain", position_lower_curtain)

        elif isinstance(node, OpeningDevice):
            if status_position_is_concrete:
                node_changed |= _set_node_property(node, "position", status_position)

        if (
            isinstance(node, OpeningDevice)
            and status_position_is_concrete
            and frame.run_status == RunStatus.EXECUTION_COMPLETED
        ):
            node_changed |= self._clear_opening_device_motion(node)

        if node_changed:
            await node.after_update()

    async def _update_opening_device_status(
        self,
        node: OpeningDevice,
        frame: (
            FrameGetAllNodesInformationNotification
            | FrameNodeStatePositionChangedNotification
        ),
    ) -> bool:

        position = Position(frame.current_position)
        target = Position(frame.target)
        frame_position_is_concrete = self._is_concrete_position(position)
        comparison_position_is_concrete = frame_position_is_concrete
        target_is_concrete = self._is_concrete_position(target)
        frame_indicates_motion = (
            frame.state == OperatingState.EXECUTING
            or frame.remaining_time > 0
        )

        comparison_position = position
        if not comparison_position_is_concrete and self._is_concrete_position(node.position):
            comparison_position = node.position
            comparison_position_is_concrete = True

        node_changed = False

        if (
            comparison_position_is_concrete
            and target_is_concrete
            and comparison_position.position > target.position
            and frame_indicates_motion
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
                node.name, comparison_position, target,
                frame.remaining_time,
                node.estimated_completion.strftime("%Y-%m-%d %H:%M:%S")
            )

        elif (
            comparison_position_is_concrete
            and target_is_concrete
            and comparison_position.position < target.position
            and frame_indicates_motion
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
                node.name, comparison_position, target,
                frame.remaining_time,
                node.estimated_completion.strftime("%Y-%m-%d %H:%M:%S")
            )

        elif (
            not frame_position_is_concrete
            and target_is_concrete
            and self._is_concrete_position(node.target)
            and node.target != target
            and frame_indicates_motion
        ):
            # node.target is updated in _update_node_main_parameter after this method returns.
            if node.target.position > target.position:
                node_changed |= _set_node_property(node, "is_opening", True)
                node_changed |= _set_node_property(node, "is_closing", False)
            else:
                node_changed |= _set_node_property(node, "is_closing", True)
                node_changed |= _set_node_property(node, "is_opening", False)
            node.state_received_at = datetime.datetime.now()
            node.estimated_completion = (
                node.state_received_at
                + datetime.timedelta(0, frame.remaining_time)
            )
            PYVLXLOG.debug(
                "%s changed motion target while current position is unavailable (%s->%s),"
                " estimated completion in %ss at %s",
                node.name,
                node.target,
                target,
                frame.remaining_time,
                node.estimated_completion.strftime("%Y-%m-%d %H:%M:%S"),
            )

        elif (
            frame_indicates_motion
            and target_is_concrete
            and (node.is_opening or node.is_closing)
            and not (
                # Cached position already reached an open/closed extreme that matches the
                # target: treat the motion as complete even when the gateway still flags
                # the device as executing (observed on garage doors after the limit
                # switch trips: a final EXECUTING frame can arrive with stale
                # remaining_time > 0, which would otherwise trap is_closing/is_opening).
                # Use the semantic Position.closed/open accessors so devices that report
                # closed-with-tolerance (e.g. Velux SML, which does not necessarily hit
                # exactly Parameter.MAX) still match the escape.
                self._is_concrete_position(node.position)
                and (
                    (target.closed and node.position.closed)
                    or (target.open and node.position.open)
                )
            )
        ):
            node.state_received_at = datetime.datetime.now()
            node.estimated_completion = (
                node.state_received_at
                + datetime.timedelta(0, frame.remaining_time)
            )
            PYVLXLOG.debug(
                "%s keeps previous motion state while current position is unavailable (%s->%s),"
                " estimated completion in %ss at %s",
                node.name,
                position,
                target,
                frame.remaining_time,
                node.estimated_completion.strftime("%Y-%m-%d %H:%M:%S"),
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
        frame: (
            FrameGetAllNodesInformationNotification
            | FrameNodeStatePositionChangedNotification
        ),
    ) -> bool:

        node_changed = False
        if isinstance(node, OpeningDevice):
            position = Position(frame.current_position)
            target = Position(frame.target)
            frame_indicates_motion = (
                frame.state == OperatingState.EXECUTING
                or frame.remaining_time > 0
            )
            if self._is_concrete_position(position):
                node_changed |= _set_node_property(node, "position", position)
                node_changed |= _set_node_property(node, "target", target)
            elif self._is_concrete_position(target) and frame_indicates_motion:
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
        frame: (
            FrameGetAllNodesInformationNotification
            | FrameNodeStatePositionChangedNotification
        ),
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

        # Gates and garage doors frequently keep current_position = IGNORE for the
        # entire travel and only signal completion via this command-run-status
        # frame (run_status = COMPLETED/FAILED). Without clearing motion here,
        # is_opening/is_closing would only fall back to False on the next polled
        # status sweep, leaving the entity stuck in opening/closing for up to a
        # full heartbeat period.
        if (
            isinstance(node, OpeningDevice)
            and frame.run_status in (RunStatus.EXECUTION_COMPLETED, RunStatus.EXECUTION_FAILED)
            and (node.is_opening or node.is_closing)
        ):
            # EXECUTION_COMPLETED is the gateway's signal that the active
            # command run has finished for this node and is therefore
            # authoritative for our motion tracking.
            #
            # Only on a clean completion (COMMAND_COMPLETED_OK) can we
            # additionally assume the device actually reached its target;
            # in that case we sync the cached position so consumers don't
            # briefly see a stale pre-move value when the IGNORE-mode
            # position frames never updated it during travel. Other
            # status_reply values mean the run was pre-empted before
            # reaching the target (e.g. COMMAND_OVERRULED by a new
            # command), so the position must stay at whatever the latest
            # state frame established. EXECUTION_FAILED is similar — the
            # device did not reach the target.
            #
            # Sync source preference: the CRSN payload itself carries the
            # final main-parameter value, which is more up-to-date than
            # the cached node.target if the matching state frame has not
            # arrived yet. Fall back to node.target only when the payload
            # is not a concrete MP value.
            if (
                frame.run_status == RunStatus.EXECUTION_COMPLETED
                and frame.status_reply == StatusReply.COMMAND_COMPLETED_OK
            ):
                synced_position: Position | None = None
                if (
                    frame.node_parameter == NodeParameter.MP.value
                    and frame.parameter_value is not None
                ):
                    candidate = Position(position=frame.parameter_value)
                    if self._is_concrete_position(candidate):
                        synced_position = candidate
                if synced_position is None and self._is_concrete_position(node.target):
                    synced_position = node.target
                if synced_position is not None:
                    node_changed |= _set_node_property(
                        node, "position", synced_position
                    )
            node_changed |= self._clear_opening_device_motion(node)
            PYVLXLOG.debug(
                "%s motion cleared after command run finished (%s)",
                node.name,
                frame.run_status.name,
            )

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
