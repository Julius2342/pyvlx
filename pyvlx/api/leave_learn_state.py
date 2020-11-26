"""Module for handling the login to API."""
from ..log import PYVLXLOG
from .api_event import ApiEvent
from .frames import (FrameLeaveLearnStateRequest,
                     FrameLeaveLearnStateConfirmation, LeaveLearnStateConfirmationStatus)


class DtoLeaveLearnState:
    """Dataobject to hold KLF200 Data."""

    def __init__(self, status=None):
        """Initialize DtoLeaveLearnState class."""
        self.status = status

    @property
    def status_name(self):
        """Return status as human readable string."""
        return LeaveLearnStateConfirmationStatus(self.status_name).name

    def __str__(self):
        """Return human readable string."""
        return (
            '<{} status="{}" status_name="{}"/>'.format(
                type(self).__name__, self.status, self.status_name
            )
        )


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
        if self.status == LeaveLearnStateConfirmationStatus.FAILED:
            PYVLXLOG.warning(
                'Failed to leave learn state'
            )
            self.success = False
        if self.status == LeaveLearnStateConfirmationStatus.SUCCESSFUL:
            self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameLeaveLearnStateRequest()
