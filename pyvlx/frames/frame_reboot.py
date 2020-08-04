"""Module for reboot frame classes."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameGatewayRebootRequest(FrameBase):
    """Frame for requesting version."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_REBOOT_REQ)

    def __str__(self):
        """Return human readable string."""
        return "<FrameGatewayRebootRequest/>"


class FrameGatewayRebootConfirmation(FrameBase):
    """Frame for response for get version requests."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_REBOOT_CFM)

    def __str__(self):
        """Return human readable string."""
        return "<FrameGatewayRebootConfirmation/>"
