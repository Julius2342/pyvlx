"""Module for leave learn state frame classes."""
from pyvlx.const import Command, LeaveLearnStateConfirmationStatus

from .frame import FrameBase


class FrameLeaveLearnStateRequest(FrameBase):
    """Frame for leaving learn state request."""

    PAYLOAD_LEN = 0

    def __init__(self) -> None:
        """Init Frame."""
        super().__init__(Command.GW_LEAVE_LEARN_STATE_REQ)

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{}/>'.format(type(self).__name__)


class FrameLeaveLearnStateConfirmation(FrameBase):
    """Frame for confirmation for leaving learn State."""

    PAYLOAD_LEN = 1

    def __init__(self, status: int = 0):
        """Init Frame."""
        super().__init__(Command.GW_LEAVE_LEARN_STATE_CFM)
        self.status = LeaveLearnStateConfirmationStatus(status)

    def get_payload(self) -> bytes:
        """Return Payload."""
        return bytes([self.status.value])

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.status = LeaveLearnStateConfirmationStatus(payload[0])

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} status="{}"/>'.format(type(self).__name__, self.status)
