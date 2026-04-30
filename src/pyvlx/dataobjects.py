"""Module for Dataobjects."""
import time
from datetime import datetime

from .const import (
    DHCPParameter, GatewayState, GatewaySubState,
    LeaveLearnStateConfirmationStatus)


class DtoLocalTime:
    """Dataobject to hold KLF200 Time Data."""

    def __init__(self, utctime: datetime | None = None, localtime: datetime | None = None):
        """Initialize DtoLocalTime class."""
        if utctime is None:
            utctime = datetime.fromtimestamp(0)
        if localtime is None:
            localtime = datetime.fromtimestamp(0)
        self.utctime = utctime
        self.localtime = localtime

    def __str__(self) -> str:
        """Return human readable string."""
        return f'<{type(self).__name__} utctime="{self.utctime}" localtime="{self.localtime}"/>'

    def from_payload(self, payload: bytes) -> None:
        """Build the Dto From Data."""
        self.utctime = datetime.fromtimestamp(int.from_bytes(payload[0:4], "big"))
        weekday = payload[11] - 1
        if weekday == -1:
            weekday = 6

        self.localtime = datetime.fromtimestamp(time.mktime(
            (int.from_bytes(payload[9:11], byteorder='big') + 1900,  # Year
             payload[8],  # month
             payload[7],  # day
             payload[6],  # hour
             payload[5],  # minute
             payload[4],  # second
             weekday,
             int.from_bytes(payload[12:14], byteorder='big'),  # day of year
             int.from_bytes(payload[14:15], byteorder='big', signed=True))))

    def to_payload(self) -> bytes:
        """Build the Dto From Data."""
        payload = b''
        payload = int(self.utctime.timestamp()).to_bytes(4, byteorder='big')
        payload += self.localtime.second.to_bytes(1, "big")
        payload += self.localtime.minute.to_bytes(1, "big")
        payload += self.localtime.hour.to_bytes(1, "big")
        payload += self.localtime.day.to_bytes(1, "big")
        payload += self.localtime.month.to_bytes(1, "big")
        payload += (self.localtime.year - 1900).to_bytes(2, "big")
        if (weekday := self.localtime.weekday()) == 6:
            payload += (0).to_bytes(1, "big")
        else:
            payload += (weekday + 1).to_bytes(1, "big")
        payload += self.localtime.timetuple().tm_yday.to_bytes(2, "big")
        payload += (self.localtime.timetuple().tm_isdst).to_bytes(1, "big", signed=True)
        return payload


class DtoNetworkSetup:
    """Dataobject to hold KLF200 Network Setup."""

    def __init__(self,
                 ipaddress: str | None = None,
                 gateway: str | None = None,
                 netmask: str | None = None,
                 dhcp: DHCPParameter | None = None):
        """Initialize DtoNetworkSetup class."""
        self.ipaddress = ipaddress
        self.gateway = gateway
        self.netmask = netmask
        self.dhcp = dhcp

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            f'<{type(self).__name__} ipaddress="{self.ipaddress}" netmask="{self.netmask}" '
            f'gateway="{self.gateway}"  dhcp="{self.dhcp}"/>'
        )


class DtoProtocolVersion:
    """KLF 200 Dataobject for Protocol version."""

    def __init__(self, majorversion: int | None = None, minorversion: int | None = None):
        """Initialize DtoProtocolVersion class."""
        self.majorversion = majorversion
        self.minorversion = minorversion

    def __str__(self) -> str:
        """Return human readable string."""
        return f'<{type(self).__name__} majorversion="{self.majorversion}" minorversion="{self.minorversion}"/>'


class DtoState:
    """Data Object for Gateway State."""

    def __init__(self, gateway_state: GatewayState | None = None, gateway_sub_state: GatewaySubState | None = None):
        """Initialize DtoState class."""
        self.gateway_state = gateway_state
        self.gateway_sub_state = gateway_sub_state

    def __str__(self) -> str:
        """Return human readable string."""
        return f'<{type(self).__name__} gateway_state="{self.gateway_state}" gateway_sub_state="{self.gateway_sub_state}"/>'


class DtoVersion:
    """Object for KLF200 Version Information."""

    def __init__(self,
                 softwareversion: str | None = None,
                 hardwareversion: int | None = None,
                 productgroup: int | None = None,
                 producttype: int | None = None):
        """Initialize DtoVersion class."""
        self.softwareversion = softwareversion
        self.hardwareversion = hardwareversion
        self.productgroup = productgroup
        self.producttype = producttype

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            f'<{type(self).__name__} softwareversion="{self.softwareversion}" hardwareversion="{self.hardwareversion}" '
            f'productgroup="{self.productgroup}" producttype="{self.producttype}"/>'
        )


class DtoLeaveLearnState:
    """Dataobject to hold KLF200 Data."""

    def __init__(self, status: LeaveLearnStateConfirmationStatus | None = None):
        """Initialize DtoLeaveLearnState class."""
        self.status = status

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            f'<{type(self).__name__} status="{self.status}"/>'
        )
