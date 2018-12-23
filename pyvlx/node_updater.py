"""Module for updating nodes via frames."""
from .frames import FrameNodeStatePositionChangedNotification
from .log import PYVLXLOG
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
            try:
                node = self.pyvlx.nodes[frame.node_id]
            except IndexError:
                PYVLXLOG.warning("Could not access node with id %i", frame.node_id)
            else:
                if isinstance(node, OpeningDevice):
                    node.position = Position(frame.current_position)
                    await node.after_update()
