"""Module for updating nodes via frames."""
from .frames import FrameNodeStatePositionChangedNotification
from .opening_device import OpeningDevice

class NodeUpdater():

    def __init__(self, pyvlx):
        """Initialize NodeUpdater object."""
        self.pyvlx = pyvlx

    async def process_frame(self, frame):
        """Update nodes via frame, usually received by house monitor."""
        if isinstance(frame, FrameNodeStatePositionChangedNotification):
            node = self.pyvlx.nodes[frame.node_id]
            if isinstance(node, OpeningDevice):
                node.position = frame.current_position
                await node.after_update()
