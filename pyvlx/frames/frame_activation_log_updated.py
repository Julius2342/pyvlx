"""Module for error notification."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameActivationLogUpdatedNotification(FrameBase):
    """Frame for error notification."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_ACTIVATION_LOG_UPDATED_NTF)
