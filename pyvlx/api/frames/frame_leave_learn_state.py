"""Module for leave learn state frame classes."""
from enum import Enum
from ...const import Command
from .frame import FrameBase

class LeaveLearnStateConfirmationStatus(Enum):
    """Enum class for status of password enter confirmation."""
    FAILED = 0
    SUCCESSFUL = 1

class FrameLeaveLearnStateRequest(FrameBase):
    """Frame for leaving learn state request."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_LEAVE_LEARN_STATE_REQ)

    def __str__(self):
        """Return human readable string."""
        return "<FrameLeaveLearnStateRequest/>"



class FrameLeaveLearnStateConfirmation(FrameBase):
    """Frame for confirmation for leaving learn State."""

    PAYLOAD_LEN = 1

    def __init__(self, status=0):
        """Init Frame."""
        super().__init__(Command.GW_LEAVE_LEARN_STATE_CFM)
        self.status = LeaveLearnStateConfirmationStatus(status)

    def get_payload(self):
        """Return Payload."""
        return bytes([self.status.value])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.status = LeaveLearnStateConfirmationStatus(payload[0])

    def __str__(self):
        """Return human readable string."""
        return "<{} status={}/>".format(self.__class__.__name__, self.status)
