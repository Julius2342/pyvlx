"""Module for get node information from gateway."""
from enum import Enum

from pyvlx.const import (
    Command, NodeParameter, RunStatus, StatusReply, StatusType)
from pyvlx.exception import PyVLXException
from pyvlx.parameter import Parameter

from .frame import FrameBase


class FrameStatusRequestRequest(FrameBase):
    """Frame for status request request."""

    PAYLOAD_LEN = 26

    def __init__(self, session_id=None, node_ids=None):
        """Init Frame."""
        super().__init__(Command.GW_STATUS_REQUEST_REQ)
        self.session_id = session_id
        self.node_ids = node_ids
        self.status_type = StatusType.REQUEST_CURRENT_POSITION
        self.fpi1 = 254     # Request FP1 to FP7
        self.fpi2 = 0

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([len(self.node_ids)])      # index array count
        ret += bytes(self.node_ids) + bytes(20 - len(self.node_ids))
        ret += bytes([self.status_type.value])
        ret += bytes([self.fpi1])
        ret += bytes([self.fpi2])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        len_node_ids = payload[2]
        if len_node_ids > 20:
            raise PyVLXException("command_send_request_wrong_node_length")
        self.node_ids = []
        for i in range(len_node_ids):
            self.node_ids.append(payload[3] + i)

        self.status_type = StatusType(payload[23])
        self.fpi1 = payload[24]
        self.fpi2 = payload[25]

    def __str__(self):
        """Return human readable string."""
        return (
            '<{} session_id="{}" node_ids="{}" '
            'status_type="{}" fpi1="{}" fpi2="{}"/>'.format(
                type(self).__name__, self.session_id,
                self.node_ids,
                self.status_type, self.fpi1, self.fpi2
            )
        )


class StatusRequestStatus(Enum):
    """Enum for status request status."""

    REJECTED = 0
    ACCEPTED = 1


class FrameStatusRequestConfirmation(FrameBase):
    """Frame for confirmation for status request request."""

    PAYLOAD_LEN = 3

    def __init__(self, session_id=None, status=None):
        """Init Frame."""
        super().__init__(Command.GW_STATUS_REQUEST_CFM)
        self.session_id = session_id
        self.status = status

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        ret += bytes([self.status.value])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.status = StatusRequestStatus(payload[2])

    def __str__(self):
        """Return human readable string."""
        return '<{} session_id="{}" status="{}"/>'.format(
            type(self).__name__, self.session_id, self.status
        )


class FrameStatusRequestNotification(FrameBase):
    """Frame for notification of status request request."""

    # PAYLOAD_LEN = 59
    # No PAYLOAD_LEN because it is variable depending on StatusType

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_STATUS_REQUEST_NTF)
        self.session_id = 0
        self.status_id = 0
        self.node_id = 0
        self.run_status = RunStatus.EXECUTION_COMPLETED
        self.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        self.status_type = StatusType.REQUEST_TARGET_POSITION
        self.status_count = 0
        self.parameter_data = {}
        self.target_position = Parameter()
        self.current_position = Parameter()
        self.remaining_time = 0
        self.last_master_execution_address = 0
        self.last_command_originator = 0

    def get_payload(self):
        """Return Payload."""
        payload = bytes()
        payload += bytes([self.session_id >> 8 & 255, self.session_id & 255])
        payload += bytes([self.status_id])
        payload += bytes([self.node_id])
        payload += bytes([self.run_status.value])
        payload += bytes([self.status_reply.value])
        payload += bytes([self.status_type.value])
        if self.status_type == StatusType.REQUEST_MAIN_INFO:
            payload += bytes(self.target_position.raw)
            payload += bytes(self.current_position.raw)
            payload += bytes([self.remaining_time >> 8 & 255, self.remaining_time & 255])
            payload += bytes([
                self.last_master_execution_address >> 16 & 255,
                self.last_master_execution_address >> 8 & 255,
                self.last_master_execution_address & 255
            ])

            payload += bytes([self.last_command_originator])
        else:
            payload += bytes([self.status_count])
            keys = self.parameter_data.keys()
            for key in keys:
                payload += bytes([key])
                payload += bytes(self.parameter_data[key].raw)
            payload += bytes(51 - len(self.parameter_data))

        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.session_id = payload[0] * 256 + payload[1]
        self.status_id = payload[2]
        self.node_id = payload[3]
        self.run_status = RunStatus(payload[4])
        self.status_reply = StatusReply(payload[5])
        self.status_type = StatusType(payload[6])
        if self.status_type == StatusType.REQUEST_MAIN_INFO:
            self.target_position = Parameter(payload[7:8])
            self.current_position = Parameter(payload[9:10])
            self.remaining_time = payload[11] * 256 + payload[12]
            self.last_master_execution_address = payload[13:16]
            self.last_command_originator = payload[17]
        else:
            self.status_count = payload[7]
            for i in range(8, 8 + self.status_count*3, 3):
                self.parameter_data.update({NodeParameter(payload[i]): Parameter(payload[i+1:i+3])})

    def __str__(self):
        """Return human readable string."""
        if self.status_type == StatusType.REQUEST_MAIN_INFO:
            return (
                '<{} session_id="{}" status_id="{}" '
                'node_id="{}" run_status="{}" status_reply="{}" status_type="{}" target_position="{}" '
                'current_position="{}" remaining_time="{}" last_master_execution_address="{}" last_command_originator="{}"/>'.format(
                    type(self).__name__,
                    self.session_id,
                    self.status_id,
                    self.node_id,
                    self.run_status,
                    self.status_reply,
                    self.status_type,
                    self.target_position,
                    self.current_position,
                    self.remaining_time,
                    self.last_master_execution_address,
                    self.last_command_originator,
                )
            )

        parameter_data_str = ""
        for key, value in self.parameter_data.items():
            parameter_data_str += "%s: %s, " % (
                str(key),
                str(value),
            )

        return (
            '<{} session_id="{}" status_id="{}" '
            'node_id="{}" run_status="{}" status_reply="{}" status_type="{}" status_count="{}" '
            'parameter_data="{}"/>'.format(
                type(self).__name__,
                self.session_id,
                self.status_id,
                self.node_id,
                self.run_status,
                self.status_reply,
                self.status_type,
                self.status_count,
                parameter_data_str
            )
        )
