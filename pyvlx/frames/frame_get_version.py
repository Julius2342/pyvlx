"""Module for get version frame classes."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameGetVersionRequest(FrameBase):
    """Frame for requesting version."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_VERSION_REQ)


class FrameGetVersionConfirmation(FrameBase):
    """Frame for response for get version requests."""

    PAYLOAD_LEN = 9

    def __init__(self, software_version=bytes(6), hardware_version=0):
        """Init Frame."""
        super().__init__(Command.GW_GET_VERSION_CFM)
        if isinstance(software_version, str):
            software_version = bytes(int(c) for c in software_version.split("."))
        self._software_version = software_version
        self.hardware_version = hardware_version
        self.product_group = 14
        self.product_type = 3

    @property
    def version(self):
        """Return formatted version."""
        return "{}: Software version: {}, hardware version: {}".format(
            self.product, self.software_version, self.hardware_version)

    @property
    def software_version(self):
        """Return software version as human readable string."""
        return '.'.join(str(c) for c in self._software_version)

    @property
    def product(self):
        """Return product as human readable string."""
        if self.product_group == 14 and self.product_type == 3:
            return "KLF 200"
        return "Unknown Product: {}:{}".format(self.product_group, self.product_type)

    def get_payload(self):
        """Return Payload."""
        ret = self._software_version
        ret += bytes([self.hardware_version, self.product_group, self.product_type])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self._software_version = payload[0:6]
        self.hardware_version = payload[6]
        self.product_group = payload[7]
        self.product_type = payload[8]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetVersionConfirmation software_version="{}" ' \
            'harware_version="{}" product="{}"/>'.format(
                self.software_version, self.hardware_version,
                self.product)
