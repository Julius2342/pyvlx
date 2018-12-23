"""Module for sending command to gw."""
from enum import Enum

from pyvlx.const import Command, Originator, Priority
from pyvlx.exception import PyVLXException
from pyvlx.parameter import Parameter

from .frame import FrameBase


class FrameCommandSendRequest(FrameBase):
    """Frame for sending command to gw."""

    PAYLOAD_LEN = 66

    def __init__(self, node_ids=None, parameter=Parameter(), session_id=None, originator=Originator.USER):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_SEND_REQ)
        self.node_ids = node_ids
        self.parameter = parameter
        self.session_id = session_id
        self.originator = originator
        self.priority = Priority.USER_LEVEL_2

    def get_payload(self):
        """Return Payload."""
        # Session id
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.originator.value])
        ret += bytes([self.priority.value])
        ret += bytes([0])  # ParameterActive pointing to main parameter (MP)
        # FPI 1+2
        ret += bytes([0])
        ret += bytes([0])

        # Main parameter + functional parameter
        ret += bytes(self.parameter)
        ret += bytes(32)

        # Nodes array: Number of nodes + node array + padding
        ret += bytes([len(self.node_ids)])  # index array count
        ret += bytes(self.node_ids) + bytes(20-len(self.node_ids))

        # Priority  Level Lock
        ret += bytes([0])
        # Priority Level information 1+2
        ret += bytes([0, 0])
        # Locktime
        ret += bytes([0])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0]*256 + payload[1]
        self.originator = Originator(payload[2])
        self.priority = Priority(payload[3])

        len_node_ids = payload[41]
        if len_node_ids > 20:
            raise PyVLXException("command_send_request_wrong_node_length")
        self.node_ids = []
        for i in range(len_node_ids):
            self.node_ids.append(payload[42] + i)

        self.parameter = Parameter(payload[7:9])

    def __str__(self):
        """Return human readable string."""
        return '<FrameCommandSendRequest node_ids={} parameter="{}" session_id={} originator={}/>'.format(
            self.node_ids, self.parameter, self.session_id,
            self.originator)


class CommandSendConfirmationStatus(Enum):
    """Enum class for status of command send confirmation."""

    REJECTED = 0
    ACCEPTED = 1


class FrameCommandSendConfirmation(FrameBase):
    """Frame for confirmation of command send frame."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id=None, status=None):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_SEND_CFM)
        self.session_id = session_id
        self.status = status

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.status.value])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0]*256 + payload[1]
        self.status = CommandSendConfirmationStatus(payload[2])

    def __str__(self):
        """Return human readable string."""
        return '<FrameCommandSendConfirmation session_id={} status={}/>'.format(self.session_id, self.status)


class FrameCommandRunStatusNotification(FrameBase):
    """Frame for run status notification in scope of command send frame."""

    PAYLOAD_LEN = 13

    def __init__(self, session_id=None, status_id=None, index_id=None, node_parameter=None, parameter_value=None):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_RUN_STATUS_NTF)
        self.session_id = session_id
        self.status_id = status_id
        self.index_id = index_id
        self.node_parameter = node_parameter
        self.parameter_value = parameter_value

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.status_id])
        ret += bytes([self.index_id])
        ret += bytes([self.node_parameter])
        ret += bytes([self.parameter_value >> 8 & 255, self.parameter_value & 255])

        # XXX: Missing implementation of run_status, status_reply and information_code
        ret += bytes(6)
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0]*256 + payload[1]
        self.status_id = payload[2]
        self.index_id = payload[3]
        self.node_parameter = payload[4]
        self.parameter_value = payload[5]*256 + payload[6]

    def __str__(self):
        """Return human readable string."""
        return \
            '<FrameCommandRunStatusNotification session_id={} status_id={} ' \
            'index_id={} node_parameter={} parameter_value={}/>'.format(
                self.session_id, self.status_id, self.index_id,
                self.node_parameter, self.parameter_value)


class FrameCommandRemainingTimeNotification(FrameBase):
    """Frame for notification of remaining time in scope of command send frame."""

    PAYLOAD_LEN = 6

    def __init__(self, session_id=None, index_id=None, node_parameter=None, seconds=0):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_REMAINING_TIME_NTF)
        self.session_id = session_id
        self.index_id = index_id
        self.node_parameter = node_parameter
        self.seconds = seconds

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.index_id])
        ret += bytes([self.node_parameter])
        ret += bytes([self.seconds >> 8 & 255, self.seconds & 255])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0]*256 + payload[1]
        self.index_id = payload[2]
        self.node_parameter = payload[3]
        self.seconds = payload[4]*256 + payload[5]

    def __str__(self):
        """Return human readable string."""
        return \
            '<FrameCommandRemainingTimeNotification session_id={} index_id={} ' \
            'node_parameter={} seconds={}/>'.format(
                self.session_id, self.index_id, self.node_parameter, self.seconds)


class FrameSessionFinishedNotification(FrameBase):
    """Frame for notification of session finishid in scope of command send frame."""

    PAYLOAD_LEN = 2

    def __init__(self, session_id=None):
        """Init Frame."""
        super().__init__(Command.GW_SESSION_FINISHED_NTF)
        self.session_id = session_id

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0]*256 + payload[1]

    def __str__(self):
        """Return human readable string."""
        return '<FrameSessionFinishedNotification session_id={} />'.format(self.session_id)
