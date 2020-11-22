"""Module for retrieving gateway state from API."""
from .api_event import ApiEvent
from .frames import FrameGetStateConfirmation, FrameGetStateRequest, GatewayState, GatewaySubState

class DtoState:
    """Data Object for Gateway State."""

    def __init__(self, gateway_state=None, gateway_sub_state=None):
        self.gateway_state = gateway_state
        self.gateway_sub_state = gateway_sub_state

    @property
    def gateway_state_name(self):
        """Return gateway_state as human readable string."""
        return GatewayState(self.gateway_state).name

    @property
    def gateway_sub_state_name(self):
        """Return gateway_sub_state as human readable string."""
        return GatewaySubState(self.gateway_sub_state).name

    def __str__(self):
        """Return human readable string."""
        return (
            '<{} gateway_state="{}" gateway_state_name="{}" gateway_sub_state="{}" '
            'gateway_sub_state=_name"{}"/>'.format(
                type(self).__name__, self.gateway_state, self.gateway_state_name,
                self.gateway_sub_state, self.gateway_sub_state_name
            )
        )


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
        """Deprecated: Return Gateway State as human readable string."""
        return self.state.gateway_state

    @property
    def gateway_sub_state(self):
        """Deprecated: Return Gateway Sub State as human readable string."""
        return self.state.gateway_sub_state
        