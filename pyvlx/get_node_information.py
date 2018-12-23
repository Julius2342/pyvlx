"""Module for retrieving node information from API."""
from .api_event import ApiEvent
from .frames import (
    FrameGetNodeInformationConfirmation, FrameGetNodeInformationNotification,
    FrameGetNodeInformationRequest)


class GetNodeInformation(ApiEvent):
    """Class for retrieving node informationfrom API."""

    def __init__(self, pyvlx, node_id):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.success = False
        self.notification_frame = None

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetNodeInformationConfirmation) and frame.node_id == self.node_id:
            # We are still waiting for GetNodeInformationNotification
            return False
        if isinstance(frame, FrameGetNodeInformationNotification) and frame.node_id == self.node_id:
            self.notification_frame = frame
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetNodeInformationRequest(node_id=self.node_id)
