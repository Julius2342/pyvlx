"""Module for handling the login to API."""
from .api_event import ApiEvent
from .log import PYVLXLOG
from .frames import (
    FramePasswordEnterConfirmation, FramePasswordEnterRequest,
    PasswordEnterConfirmationStatus)


class Login(ApiEvent):
    """Class for handling login to API."""

    def __init__(self, pyvlx, password):
        """Initialize login class."""
        super().__init__(pyvlx=pyvlx)
        self.password = password
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FramePasswordEnterConfirmation):
            return False
        if frame.status == PasswordEnterConfirmationStatus.FAILED:
            PYVLXLOG.warning('Failed to authenticate with password "%s****"', self.password[:2])
            self.success = False
        if frame.status == PasswordEnterConfirmationStatus.SUCCESSFUL:
            self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FramePasswordEnterRequest(password=self.password)
