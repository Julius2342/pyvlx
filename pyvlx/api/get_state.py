"""Module for retrieving gateway state from API."""
from typing import TYPE_CHECKING, Optional

from pyvlx.const import GatewayState, GatewaySubState
from pyvlx.dataobjects import DtoState

from .api_event import ApiEvent
from .frames import FrameBase, FrameGetStateConfirmation, FrameGetStateRequest

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetState(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize GetState class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.state = DtoState()

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetStateConfirmation):
            return False
        self.success = True
        self.state = DtoState(frame.gateway_state, frame.gateway_sub_state)
        return True

    def request_frame(self) -> FrameGetStateRequest:
        """Construct initiating frame."""
        return FrameGetStateRequest()

    @property
    def gateway_state(self) -> Optional[GatewayState]:
        """Return Gateway State as human readable string. Deprecated."""
        return self.state.gateway_state

    @property
    def gateway_sub_state(self) -> Optional[GatewaySubState]:
        """Return Gateway Sub State as human readable string. Deprecated."""
        return self.state.gateway_sub_state
