"""Module for password enter frame classes."""
from enum import Enum

from pyvlx.const import Command
from pyvlx.exception import PyVLXException
from pyvlx.string_helper import bytes_to_string, string_to_bytes

from .frame import FrameBase


class FramePasswordEnterRequest(FrameBase):
    """Frame for sending password enter request."""

    MAX_SIZE = 32
    PAYLOAD_LEN = 32

    def __init__(self, password=None):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_ENTER_REQ)
        self.password = password

    def get_payload(self):
        """Return Payload."""
        if self.password is None:
            raise PyVLXException("password is none")
        if len(self.password) > self.MAX_SIZE:
            raise PyVLXException("password is too long")
        return string_to_bytes(self.password, self.MAX_SIZE)

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.password = bytes_to_string(payload)

    def __str__(self):
        """Return human readable string."""
        password_esc = None if self.password is None else '{}****'.format(self.password[:2])
        return '<FramePasswordEnterRequest password={}/>'.format(password_esc)


class PasswordEnterConfirmationStatus(Enum):
    """Enum class for status of password enter confirmation."""

    SUCCESSFUL = 0
    FAILED = 1


class FramePasswordEnterConfirmation(FrameBase):
    """Frame for confirmation for sent password."""

    PAYLOAD_LEN = 1

    def __init__(self, status=PasswordEnterConfirmationStatus.SUCCESSFUL):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_ENTER_CFM)
        self.status = status

    def get_payload(self):
        """Return Payload."""
        return bytes([self.status.value])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.status = PasswordEnterConfirmationStatus(payload[0])

    def __str__(self):
        """Return human readable string."""
        return '<FramePasswordEnterConfirmation status=\'{}\'/>'.format(self.status)
