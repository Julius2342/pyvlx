"""Helper module for Node objects."""
from .const import NodeTypeWithSubtype


def convert_frame_to_node(frame):
    """Convert FrameGet[All]Node[s]InformationNotification into Node object."""
    if frame.node_type == NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR:
        return "WINDOW"
    print("{} not implemented", format(frame.node_type))
    return None
