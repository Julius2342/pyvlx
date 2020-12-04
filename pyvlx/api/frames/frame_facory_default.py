"""Module for reboot frame classes."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameGatewayFactoryDefaultRequest(FrameBase):
    """Frame for requesting factory reset."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_SET_FACTORY_DEFAULT_REQ)

    def __str__(self):
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)


class FrameGatewayFactoryDefaultConfirmation(FrameBase):
    """Frame for response for factory reset."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_SET_FACTORY_DEFAULT_CFM)

    def __str__(self):
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)
