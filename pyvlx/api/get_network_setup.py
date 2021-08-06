"""Module for retrieving gateway state from API."""
from pyvlx.dataobjects import DtoNetworkSetup

from .api_event import ApiEvent
from .frames import (
    FrameGetNetworkSetupConfirmation, FrameGetNetworkSetupRequest)


class GetNetworkSetup(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx):
        """Initialize GetNetworkSetup class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.networksetup = DtoNetworkSetup()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetNetworkSetupConfirmation):
            return False
        self.success = True
        self.networksetup = DtoNetworkSetup(
            frame.ipaddress, frame.gateway, frame.netmask, frame.dhcp)
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetNetworkSetupRequest()
