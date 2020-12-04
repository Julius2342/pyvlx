"""Module for password enter frame classes."""
from enum import Enum

from pyvlx.const import Command
from pyvlx.exception import PyVLXException
from pyvlx.string_helper import bytes_to_string, string_to_bytes

from .frame import FrameBase


class FramePasswordChangeRequest(FrameBase):
    """Frame for sending password enter request."""

    MAX_SIZE = 32
    PAYLOAD_LEN = 64

    def __init__(self, currentpassword=None, newpassword=None):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_CHANGE_REQ)
        self.currentpassword = currentpassword
        self.newpassword = newpassword

    def get_payload(self):
        """Return Payload."""
        if self.currentpassword is None:
            raise PyVLXException("currentpassword is none")
        if self.newpassword is None:
            raise PyVLXException("newpassword is none")
        if len(self.currentpassword) > self.MAX_SIZE:
            raise PyVLXException("currentpassword is too long")
        if len(self.newpassword) > self.MAX_SIZE:
            raise PyVLXException("newpassword is too long")

        return string_to_bytes(self.currentpassword,
                               self.MAX_SIZE)+string_to_bytes(self.newpassword, self.MAX_SIZE)

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.currentpassword = bytes_to_string(payload[0:32])
        self.newpassword = bytes_to_string(payload[32:])

    def __str__(self):
        """Return human readable string."""
        currentpassword_esc = (
            None if self.currentpassword is None else "{}****".format(self.currentpassword[:2])
        )
        newpassword_esc = (
            None if self.newpassword is None else "{}****".format(self.newpassword[:2])
        )
        return ('<{} currentpassword="{}" newpassword="{}"/>'
                .format(type(self).__name__, currentpassword_esc, newpassword_esc))


class PasswordChangeConfirmationStatus(Enum):
    """Enum class for status of password change confirmation."""

    SUCCESSFUL = 0
    FAILED = 1


class FramePasswordChangeConfirmation(FrameBase):
    """Frame for confirmation for sent password."""

    PAYLOAD_LEN = 1

    def __init__(self, status=PasswordChangeConfirmationStatus.SUCCESSFUL):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_CHANGE_CFM)
        self.status = status

    def get_payload(self):
        """Return Payload."""
        return bytes([self.status.value])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.status = PasswordChangeConfirmationStatus(payload[0])

    def __str__(self):
        """Return human readable string."""
        return '<{} status="{}"/>'.format(type(self).__name__, self.status)


class FramePasswordChangeNotification(FrameBase):
    """Frame for sending password changed notification request."""

    MAX_SIZE = 32
    PAYLOAD_LEN = 32

    def __init__(self, newpassword=None):
        """Init Frame."""
        super().__init__(Command.GW_PASSWORD_CHANGE_NTF)
        self.newpassword = newpassword

    def get_payload(self):
        """Return Payload."""
        if self.newpassword is None:
            raise PyVLXException("newpassword is none")
        if len(self.newpassword) > self.MAX_SIZE:
            raise PyVLXException("newpassword is too long")

        return string_to_bytes(self.newpassword, self.MAX_SIZE)

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.newpassword = bytes_to_string(payload)

    def __str__(self):
        """Return human readable string."""
        newpassword_esc = (
            None if self.newpassword is None else "{}****".format(self.newpassword[:2])
        )
        return '<{} newpassword="{}"/>'.format(type(self).__name__, newpassword_esc)
