"""Module for updating nodes via frames."""
from .frames import FrameNodeStatePositionChangedNotification, FrameGetAllNodesInformationNotification
from .opening_device import OpeningDevice
from .parameter import Position


class NodeUpdater():
    """Class for updating nodes via incoming frames,  usually received by house monitor."""

    def __init__(self, pyvlx):
        """Initialize NodeUpdater object."""
        self.pyvlx = pyvlx

    async def process_frame(self, frame):
        """Update nodes via frame, usually received by house monitor."""
        if isinstance(frame, FrameNodeStatePositionChangedNotification):
            if frame.node_id not in self.pyvlx.nodes:
                return
            node = self.pyvlx.nodes[frame.node_id]
            if isinstance(node, OpeningDevice):
                node.position = Position(frame.current_position)
                await node.after_update()
        elif isinstance(frame, FrameGetAllNodesInformationNotification):
            if frame.node_id not in self.pyvlx.nodes:
                return
            node = self.pyvlx.nodes[frame.node_id]
            if isinstance(node, OpeningDevice):
                node.position = Position(frame.current_position)
                await node.after_update()
