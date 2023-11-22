"""Module for handling the login to API."""
from typing import TYPE_CHECKING

from pyvlx.dataobjects import DtoLeaveLearnState

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameLeaveLearnStateConfirmation, FrameLeaveLearnStateRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class LeaveLearnState(ApiEvent):
    """Class for handling leave learn state to API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize leave learn state class."""
        super().__init__(pyvlx=pyvlx)
        self.status = DtoLeaveLearnState()
        self.success = False

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameLeaveLearnStateConfirmation):
            return False
        self.status.status = frame.status
        self.success = True
        return True

    def request_frame(self) -> FrameLeaveLearnStateRequest:
        """Construct initiating frame."""
        return FrameLeaveLearnStateRequest()
