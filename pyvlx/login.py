"""Module for handling the login to API."""
from pyvlx.frame_password_enter import FramePasswordEnterRequest, FramePasswordEnterConfirmation, PasswordEnterConfirmationStatus
from pyvlx.api_event import ApiEvent


class Login(ApiEvent):
    """Class for handling login to API."""

    def __init__(self, connection, password):
        """Initialize login class."""
        super().__init__(connection)
        self.password = password
        self.success = False

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FramePasswordEnterConfirmation):
            return False
        if frame.status == PasswordEnterConfirmationStatus.FAILED:
            print("Login failed")
            self.success = False
        if frame.status == PasswordEnterConfirmationStatus.SUCCESSFUL:
            print("Login successful")
            self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FramePasswordEnterRequest(password=self.password)
