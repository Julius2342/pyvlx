"""Module for handling the login to API."""
from pyvlx.dataobjects import DtoLeaveLearnState

from .api_event import ApiEvent
from .frames import (
    FrameLeaveLearnStateConfirmation, FrameLeaveLearnStateRequest)


class LeaveLearnState(ApiEvent):
    """Class for handling leave learn state to API."""

    def __init__(self, pyvlx):
        """Initialize leave learn state class."""
        super().__init__(pyvlx=pyvlx)
        self.status = DtoLeaveLearnState()
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameLeaveLearnStateConfirmation):
            return False
        self.status = frame.status
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameLeaveLearnStateRequest()
