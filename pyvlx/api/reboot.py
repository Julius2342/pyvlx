"""Module for handling the Reboot to API."""
from ..log import PYVLXLOG
from .api_event import ApiEvent
from .frames import FrameGatewayRebootConfirmation, FrameGatewayRebootRequest



class Reboot(ApiEvent):
    """Class for handling Reboot to API."""

    def __init__(self, pyvlx):
        """Initialize Reboot class."""
        super().__init__(pyvlx=pyvlx)
        self.pyvlx = pyvlx
        self.success = False


    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGatewayRebootConfirmation):
            PYVLXLOG.warning("KLF200 is rebooting")
            self.pyvlx.connection.connected = False
            self.success = True
            return True
        return False

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGatewayRebootRequest()
