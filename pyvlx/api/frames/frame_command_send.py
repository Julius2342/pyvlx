"""Module for sending command to gw."""
from enum import Enum
from typing import List, Optional

from pyvlx.const import Command, Originator, Priority
from pyvlx.exception import PyVLXException
from pyvlx.parameter import Parameter, Position

from .frame import FrameBase


class FrameCommandSendRequest(FrameBase):
    """Frame for sending command to gw."""

    PAYLOAD_LEN = 66

    def __init__(
            self,
            node_ids: Optional[List[int]] = None,
            parameter: Parameter = Parameter(),
            active_parameter: int = 0,
            session_id: Optional[int] = None,
            originator: Originator = Originator.USER,
            **functional_parameter: bytes
    ):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_SEND_REQ)
        self.node_ids = node_ids if node_ids is not None else []
        self.parameter = parameter
        self.active_parameter = active_parameter
        self.fpi1 = 0
        self.fpi2 = 0
        self.functional_parameter = {}
        self.session_id = session_id
        self.originator = originator
        self.priority = Priority.USER_LEVEL_2
        """Set the functional parameter indicator bytes in order to show which functional
        parameters are included in the frame. Functional parameter dictionary will be checked
        for keys 'fp1' to 'fp16' to set the appropriate indicator and the corresponding
        self.functional_parameter."""
        for i in range(1, 17):
            key = "fp%s" % (i)
            if key in functional_parameter:
                self.functional_parameter[key] = functional_parameter[key]
                if i < 9:
                    self.fpi1 += 2 ** (8 - i)
                if i >= 9:
                    self.fpi2 += 2 ** (16 - i)
            else:
                self.functional_parameter[key] = bytes(2)

    def get_payload(self) -> bytes:
        """Return Payload."""
        # Session id
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.originator.value])
        ret += bytes([self.priority.value])
        ret += bytes(
            [self.active_parameter]
        )  # ParameterActive pointing to main parameter (MP)
        # FPI 1+2
        ret += bytes([self.fpi1])
        ret += bytes([self.fpi2])
        # Main parameter + functional parameter fp1 to fp3
        ret += bytes(self.parameter)
        ret += bytes(self.functional_parameter["fp1"])
        ret += bytes(self.functional_parameter["fp2"])
        ret += bytes(self.functional_parameter["fp3"])
        # Functional parameter fp4 to fp16
        ret += bytes(26)

        # Nodes array: Number of nodes + node array + padding
        ret += bytes([len(self.node_ids)])  # index array count
        ret += bytes(self.node_ids) + bytes(20 - len(self.node_ids))

        # Priority  Level Lock
        ret += bytes([0])
        # Priority Level information 1+2
        ret += bytes([0, 0])
        # Locktime
        ret += bytes([0])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.originator = Originator(payload[2])
        self.priority = Priority(payload[3])

        len_node_ids = payload[41]
        if len_node_ids > 20:
            raise PyVLXException("command_send_request_wrong_node_length")
        self.node_ids = []
        for i in range(len_node_ids):
            self.node_ids.append(payload[42] + i)

        self.parameter = Parameter(payload[7:9])

    def __str__(self) -> str:
        """Return human readable string."""
        functional_parameter = ""
        for key, value in self.functional_parameter.items():
            functional_parameter += "%s: %s, " % (
                str(key),
                Position(Parameter(bytes(value))),
            )
        return (
            '<{} node_ids="{}" active_parameter="{}" parameter="{}" functional_parameter="{}" '
            'session_id="{}" originator="{}"/>'.format(
                type(self).__name__, self.node_ids, self.active_parameter,
                self.parameter, functional_parameter,
                self.session_id, self.originator,
            )
        )


class CommandSendConfirmationStatus(Enum):
    """Enum class for status of command send confirmation."""

    REJECTED = 0
    ACCEPTED = 1


class FrameCommandSendConfirmation(FrameBase):
    """Frame for confirmation of command send frame."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id: Optional[int] = None, status: Optional[CommandSendConfirmationStatus] = None):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_SEND_CFM)
        self.session_id = session_id
        self.status = status

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        assert self.status is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.status.value])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.status = CommandSendConfirmationStatus(payload[2])

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}" status="{}"/>'.format(
            type(self).__name__, self.session_id, self.status
        )


class FrameCommandRunStatusNotification(FrameBase):
    """Frame for run status notification in scope of command send frame."""

    PAYLOAD_LEN = 13

    def __init__(
            self,
            session_id: Optional[int] = None,
            status_id: Optional[int] = None,
            index_id: Optional[int] = None,
            node_parameter: Optional[int] = None,
            parameter_value: Optional[int] = None,
    ):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_RUN_STATUS_NTF)
        self.session_id = session_id
        self.status_id = status_id
        self.index_id = index_id
        self.node_parameter = node_parameter
        self.parameter_value = parameter_value

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        assert self.status_id is not None
        ret += bytes([self.status_id])
        assert self.index_id is not None
        ret += bytes([self.index_id])
        assert self.node_parameter is not None
        ret += bytes([self.node_parameter])
        assert self.parameter_value is not None
        ret += bytes([self.parameter_value >> 8 & 255, self.parameter_value & 255])

        # XXX: Missing implementation of run_status, status_reply and information_code
        ret += bytes(6)
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.status_id = payload[2]
        self.index_id = payload[3]
        self.node_parameter = payload[4]
        self.parameter_value = payload[5] * 256 + payload[6]

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            '<{} session_id="{}" status_id="{}" '
            'index_id="{}" node_parameter="{}" parameter_value="{}"/>'.format(
                type(self).__name__, self.session_id,
                self.status_id, self.index_id,
                self.node_parameter, self.parameter_value
            )
        )


class FrameCommandRemainingTimeNotification(FrameBase):
    """Frame for notification of remaining time in scope of command send frame."""

    PAYLOAD_LEN = 6

    def __init__(self, session_id: Optional[int] = None, index_id: Optional[int] = None, node_parameter: Optional[int] = None, seconds: int = 0):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_REMAINING_TIME_NTF)
        self.session_id = session_id
        self.index_id = index_id
        self.node_parameter = node_parameter
        self.seconds = seconds

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        assert self.index_id is not None
        ret += bytes([self.index_id])
        assert self.node_parameter is not None
        ret += bytes([self.node_parameter])
        ret += bytes([self.seconds >> 8 & 255, self.seconds & 255])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.index_id = payload[2]
        self.node_parameter = payload[3]
        self.seconds = payload[4] * 256 + payload[5]

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            '<{} session_id="{}" index_id="{}" '
            'node_parameter="{}" seconds="{}"/>'.format(
                type(self).__name__, self.session_id,
                self.index_id, self.node_parameter, self.seconds
            )
        )


class FrameSessionFinishedNotification(FrameBase):
    """Frame for notification of session finishid in scope of command send frame."""

    PAYLOAD_LEN = 2

    def __init__(self, session_id: Optional[int] = None):
        """Init Frame."""
        super().__init__(Command.GW_SESSION_FINISHED_NTF)
        self.session_id = session_id

    def get_payload(self) -> bytes:
        """Return Payload."""
        assert self.session_id is not None
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        return ret

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]

    def __str__(self) -> str:
        """Return human readable string."""
        return '<{} session_id="{}"/>'.format(
            type(self).__name__, self.session_id
        )
