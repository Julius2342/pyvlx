"""Module for retrieving gateway state from API."""
from .api_event import ApiEvent
from .frames import FrameGetStateConfirmation, FrameGetStateRequest


class GetState(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx):
        """Initialize login class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.gateway_state = None
        self.gateway_sub_state = None

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetStateConfirmation):
            return False
        self.success = True
        self.gateway_state = frame.gateway_state
        self.gateway_sub_state = frame.gateway_sub_state
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetStateRequest()
