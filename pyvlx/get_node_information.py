"""Module for retrieving node information from API."""
from pyvlx.frame_get_node_information import FrameGetNodeInformationRequest, \
    FrameGetNodeInformationConfirmation, FrameGetNodeInformationNotification
from pyvlx.api_event import ApiEvent
from .node_helper import convert_frame_to_node


class GetNodeInformation(ApiEvent):
    """Class for retrieving node informationfrom API."""

    def __init__(self, connection, node_id):
        """Initialize SceneList class."""
        super().__init__(connection)
        self.node_id = node_id
        self.success = False
        self.node = None

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetNodeInformationConfirmation) and frame.node_id == self.node_id:
            # We are still waiting for GetNodeInformationNotification
            return False
        if isinstance(frame, FrameGetNodeInformationNotification) and frame.node_id == self.node_id:
            self.node = convert_frame_to_node(frame)
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetNodeInformationRequest(node_id=self.node_id)
