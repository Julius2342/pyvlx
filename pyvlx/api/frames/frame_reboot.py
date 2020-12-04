"""Module for reboot frame classes."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameGatewayRebootRequest(FrameBase):
    """Frame for requesting reboot."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_REBOOT_REQ)

    def __str__(self):
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)


class FrameGatewayRebootConfirmation(FrameBase):
    """Frame for response for reboot requests."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_REBOOT_CFM)

    def __str__(self):
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)
