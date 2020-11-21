"""Module for confirmation for setting UTC time."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameSetUTCConfirmation(FrameBase):
    """Frame for confirmation for setting UTC time."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_SET_UTC_CFM)
