"""Frames for receiving network setup from gateway."""
from enum import Enum

from ...const import Command

from .frame import FrameBase


class FrameGetNetworkSetupRequest(FrameBase):
    """Frame for requesting network setup."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_NETWORK_SETUP_REQ)


class DHCPParameter(Enum):
    """Enum class for dncp network setup of gateway."""

    DISABLE = 0x00
    ENABLE = 0x01


class FrameGetNetworkSetupConfirmation(FrameBase):
    """Frame for confirmation for get network setup requests."""

    PAYLOAD_LEN = 13

    def __init__(self, ipaddress=bytes(4), netmask=bytes(4), gateway=bytes(4),
                 dhcp=DHCPParameter.DISABLE):
        """Init Frame."""
        super().__init__(Command.GW_GET_NETWORK_SETUP_CFM)
        self._ipaddress = ipaddress
        self._netmask = netmask
        self._gateway = gateway
        self.dhcp = DHCPParameter(dhcp)

    @property
    def ipaddress(self):
        """Return ipaddress as human readable string."""
        return ".".join(str(c) for c in self._ipaddress)

    @property
    def netmask(self):
        """Return ipaddress as human readable string."""
        return ".".join(str(c) for c in self._netmask)

    @property
    def gateway(self):
        """Return ipaddress as human readable string."""
        return ".".join(str(c) for c in self._gateway)

    def get_payload(self):
        """Return Payload."""
        payload = bytes([self._ipaddress.value, self._netmask.value,
                         self._gateway.value, self.dhcp.value])
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self._ipaddress = payload[0:4]
        self._netmask = payload[4:8]
        self._gateway = payload[8:12]
        self.dhcp = DHCPParameter(payload[12])

    def __str__(self):
        """Return human readable string."""
        return '<{} ipaddress="{}" netmask="{}" gateway="{}" dhcp="{}"/>'.format(
            type(self).__name__, self.ipaddress, self.netmask, self.gateway, self.dhcp)
