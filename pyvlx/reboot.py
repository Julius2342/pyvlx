"""Module for handling the login to API."""
from .api_event import ApiEvent
from .frames import FrameGatewayRebootConfirmation, FrameGatewayRebootRequest
from .log import PYVLXLOG


class Reboot(ApiEvent):
    """Class for handling login to API."""

    def __init__(self, pyvlx):
        """Initialize login class."""
        super().__init__(pyvlx=pyvlx)
        self.pyvlx = pyvlx

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGatewayRebootConfirmation):
            PYVLXLOG.warning("KLF200 is rebooting")
            self.pyvlx.connection.connected = False
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGatewayRebootRequest()
