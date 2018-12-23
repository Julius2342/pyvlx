"""Module for get node information from gateway."""
import struct
from datetime import datetime

from pyvlx.const import Command
from pyvlx.parameter import Parameter

from .frame import FrameBase


class FrameNodeStatePositionChangedNotification(FrameBase):
    """Frame for notification of note information request."""

    PAYLOAD_LEN = 20

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_NODE_STATE_POSITION_CHANGED_NTF)
        self.node_id = 0
        self.state = 0
        self.current_position = Parameter()
        self.target = Parameter()
        self.current_position_fp1 = Parameter()
        self.current_position_fp2 = Parameter()
        self.current_position_fp3 = Parameter()
        self.current_position_fp4 = Parameter()
        self.remaining_time = 0
        self.timestamp = 0

    def get_payload(self):
        """Return Payload."""
        payload = bytes([self.node_id])
        payload += bytes([self.state])
        payload += bytes(self.current_position.raw)
        payload += bytes(self.target.raw)
        payload += bytes(self.current_position_fp1.raw)
        payload += bytes(self.current_position_fp2.raw)
        payload += bytes(self.current_position_fp3.raw)
        payload += bytes(self.current_position_fp4.raw)
        payload += bytes([self.remaining_time >> 8 & 255, self.remaining_time & 255])
        payload += struct.pack(">I", self.timestamp)
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.node_id = payload[0]
        self.state = payload[1]
        self.current_position = Parameter(payload[2:4])
        self.target = Parameter(payload[4:6])
        self.current_position_fp1 = Parameter(payload[6:8])
        self.current_position_fp2 = Parameter(payload[8:10])
        self.current_position_fp3 = Parameter(payload[10:12])
        self.current_position_fp4 = Parameter(payload[12:14])
        self.remaining_time = payload[14] * 256 + payload[15]
        # @VELUX: looks like your timestamp is wrong. Looks like
        # you are only transmitting the two lower bytes.
        self.timestamp = struct.unpack(">I", payload[16:20])[0]

    @property
    def timestamp_formatted(self):
        """Return time as human readable string."""
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')

    def __str__(self):
        """Return human readable string."""
        return '<FrameNodeStatePositionChangedNotification node_id={} ' \
            'state={} current_position=\'{}\' ' \
            'target=\'{}\' current_position_fp1=\'{}\' current_position_fp2=\'{}\' ' \
            'current_position_fp3=\'{}\' current_position_fp4=\'{}\' ' \
            'remaining_time={} time=\'{}\'/>'.format(
                self.node_id,
                self.state,
                self.current_position,
                self.target,
                self.current_position_fp1,
                self.current_position_fp2,
                self.current_position_fp3,
                self.current_position_fp4,
                self.remaining_time,
                self.timestamp_formatted)
