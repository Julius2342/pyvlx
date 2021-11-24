"""Module for updating nodes via frames."""
from .api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification, FrameStatusRequestNotification)
from .const import NodeParameter
from .lightening_device import LighteningDevice
from .log import PYVLXLOG
from .opening_device import Blind, OpeningDevice
from .parameter import Intensity, Parameter, Position


class NodeUpdater:
    """Class for updating nodes via incoming frames,  usually received by house monitor."""

    def __init__(self, pyvlx):
        """Initialize NodeUpdater object."""
        self.pyvlx = pyvlx

    async def process_frame_status_request_notification(self, frame: FrameStatusRequestNotification):
        PYVLXLOG.debug("NodeUpdater process frame: %s", frame)
        if frame.node_id not in self.pyvlx.nodes:
            return
        node = self.pyvlx.nodes[frame.node_id]
        if isinstance(node, Blind):
            if NodeParameter(0) not in frame.parameter_data:    # MP missing in frame
                return
            if NodeParameter(3) not in frame.parameter_data:    # FP3 missing in frame
                return
            position = Position(frame.parameter_data[NodeParameter(0)])
            orientation = Position(frame.parameter_data[NodeParameter(3)])
            if position.position <= Parameter.MAX:
                node.position = position
                PYVLXLOG.debug("%s position changed to: %s", node.name, position)
            if orientation.position <= Parameter.MAX:
                node.orientation = orientation
                PYVLXLOG.debug(
                    "%s orientation changed to: %s", node.name, orientation
                )

            await node.after_update()

    async def process_frame(self, frame):
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
            # KLF transmits for functional parameters basically always 'No feed-back value known’ (0xF7FF).
            # In home assistant this cause unreasonable values like -23%. Therefore a check is implemented
            # whether the frame parameter is inside the maximum range.
            if isinstance(node, Blind):
                if position.position <= Parameter.MAX:
                    node.position = position
                    PYVLXLOG.debug("%s position changed to: %s", node.name, position)
                # House Monitor delivers wrong values for FP3 parameter
                # Orientation is updated in pulse() in heartbeat.py
                # if orientation.position <= Parameter.MAX:
                #     node.orientation = orientation
                #     PYVLXLOG.debug(
                #         "%s orientation changed to: %s", node.name, orientation
                #     )
                await node.after_update()
            elif isinstance(node, OpeningDevice):
                if position.position <= Parameter.MAX:
                    node.position = position
                await node.after_update()
            elif isinstance(node, LighteningDevice):
                intensity = Intensity(frame.current_position)
                if intensity.intensity <= Parameter.MAX:
                    node.intensity = intensity
                await node.after_update()
        elif isinstance(frame, FrameStatusRequestNotification):
            await self.process_frame_status_request_notification(frame)
