"""Module for error notification."""
from enum import Enum

from pyvlx.const import Command

from .frame import FrameBase


class ErrorType(Enum):
    """Enum class for error types."""

    NotFurtherDefined = 0
    UnknownCommand = 1
    ErrorOnFrameStructure = 2
    BusBusy = 7
    BadSystemTableIndex = 8
    NotAuthenticated = 12


class FrameErrorNotification(FrameBase):
    """Frame for error notification."""

    PAYLOAD_LEN = 1

    def __init__(self, error_type=ErrorType.NotFurtherDefined):
        """Init Frame."""
        super().__init__(Command.GW_ERROR_NTF)
        self.error_type = error_type

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.error_type.value])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.error_type = ErrorType(payload[0])

    def __str__(self):
        """Return human readable string."""
        return '<FrameErrorNotification error_type=\'{}\'/>'.format(self.error_type)
