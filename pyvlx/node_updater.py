"""Module for updating nodes via frames."""
from .frames import FrameNodeStatePositionChangedNotification
from .opening_device import OpeningDevice


async def update_nodes(self, frame):
    """Update nodes via frame, usually received by house monitor."""
    if isinstance(frame, FrameNodeStatePositionChangedNotification):
        node = self.nodes[frame.node_id]
        if isinstance(node, OpeningDevice):
            node.position = frame.current_position
            await node.after_update()
