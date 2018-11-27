"""Module for requesting disabling the house status monitor."""
from pyvlx.const import Command

from .frame import FrameBase


class FrameHouseStatusMonitorDisableRequest(FrameBase):
    """Frame for requesting disabling the house status monitor."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_HOUSE_STATUS_MONITOR_DISABLE_REQ)
