"""Helper module for Node objects."""
from .const import NodeTypeWithSubtype
from .window import Window


def convert_frame_to_node(pyvlx, frame):
    """Convert FrameGet[All]Node[s]InformationNotification into Node object."""
    if frame.node_type == NodeTypeWithSubtype.WINDOW_OPENER:
        return Window(pyvlx=pyvlx, node_id=frame.node_id, name=frame.name, rain_sensor=False)
    if frame.node_type == NodeTypeWithSubtype.WINDOW_OPENER_WITH_RAIN_SENSOR:
        return Window(pyvlx=pyvlx, node_id=frame.node_id, name=frame.name, rain_sensor=True)

    print("{} not implemented", format(frame.node_type))
    return None
