"""Module for retrieving gateway state from API."""
from .api_event import ApiEvent
from .frames import FrameGetNetworkSetupConfirmation, FrameGetNetworkSetupRequest, DHCPParameter

class DtoNetworkSetup:
    def __init__(self, ipaddress = None, gateway = None, netmask = None, dhcp = None):
        self.ipaddress = ipaddress
        self.gateway = gateway
        self.netmask = netmask
        self.dhcp = dhcp

    @property
    def dhcp_name(self):
        """Return dhcp as human readable string."""
        return DHCPParameter(self.dhcp).name

    def __str__(self):
        """Return human readable string."""
        return '<DtoNetworkSetup ipaddress="{}" gateway="{}" gateway="{}"  dhcp="{}" dhcp_name="{}"/>'.format(
                self.ipaddress, self.gateway, self.gateway, self.dhcp, self.dhcp_name
        )

class GetNetworkSetup(ApiEvent):
    """Class for retrieving gateway state from API."""

    def __init__(self, pyvlx):
        """Initialize GetNetworkSetup class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.ip = DtoNetworkSetup()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetNetworkSetupConfirmation):
            return False
        self.success = True
        self.ip = DtoNetworkSetup(frame.ipaddress, frame.gateway, frame.netmask, frame.dhcp)
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetNetworkSetupRequest()
