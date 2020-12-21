"""Module for retrieving gateway state from API."""
from pyvlx.dataobjects import DtoState

from .api_event import ApiEvent
from .frames import FrameGetStateConfirmation, FrameGetStateRequest


class GetState(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx):
        """Initialize GetState class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.state = DtoState()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetStateConfirmation):
            return False
        self.success = True
        self.state = DtoState(frame.gateway_state, frame.gateway_sub_state)
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetStateRequest()

    @property
    def gateway_state(self):
        """Return Gateway State as human readable string. Deprecated."""
        return self.state.gateway_state

    @property
    def gateway_sub_state(self):
        """Return Gateway Sub State as human readable string. Deprecated."""
        return self.state.gateway_sub_state
