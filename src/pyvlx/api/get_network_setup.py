"""Module for retrieving gateway state from API."""
from typing import TYPE_CHECKING

from pyvlx.dataobjects import DtoNetworkSetup

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetNetworkSetupConfirmation, FrameGetNetworkSetupRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetNetworkSetup(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize GetNetworkSetup class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.networksetup = DtoNetworkSetup()

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetNetworkSetupConfirmation):
            return False
        self.success = True
        self.networksetup = DtoNetworkSetup(
            frame.ipaddress, frame.gateway, frame.netmask, frame.dhcp)
        return True

    def request_frame(self) -> FrameGetNetworkSetupRequest:
        """Construct initiating frame."""
        return FrameGetNetworkSetupRequest()
