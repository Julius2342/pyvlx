"""Module for retrieving node information from API."""
from .api_event import ApiEvent
from .frames import (
    FrameStatusRequestConfirmation, FrameStatusRequestNotification,
    FrameStatusRequestRequest)
from .session_id import get_new_session_id


class StatusRequest(ApiEvent):
    """Class for retrieving node informationfrom API."""

    def __init__(self, pyvlx, node_id):
        """Initialize SceneList class."""
        super().__init__(pyvlx=pyvlx)
        self.node_id = node_id
        self.success = False
        self.notification_frame = None
        self.session_id = None

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if (
                isinstance(frame, FrameStatusRequestConfirmation)
                and frame.session_id == self.session_id
        ):
            # We are still waiting for StatusRequestNotification
            return False
        if (
                isinstance(frame, FrameStatusRequestNotification)
                and frame.session_id == self.session_id
        ):
            self.notification_frame = frame
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        self.session_id = get_new_session_id()
        return FrameStatusRequestRequest(
            session_id=self.session_id,
            node_ids=[self.node_id]
        )
