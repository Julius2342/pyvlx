"""Module for get node information from gateway."""
from enum import Enum
from .frame import FrameBase
from .const import Command
# from .exception import PyVLXException
from .string_helper import bytes_to_string  # , string_to_bytes


class FrameGetNodeInformationRequest(FrameBase):
    """Frame for get node information request."""

    def __init__(self, node_id=None):
        """Init Frame."""
        super().__init__(Command.GW_GET_NODE_INFORMATION_REQ)
        self.node_id = node_id

    def get_payload(self):
        """Return Payload."""
        return bytes([self.node_id])

    def from_payload(self, payload):
        """Init frame from binary data."""
        return payload[0]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetNodeInformationRequest node_id={}/>'.format(self.node_id)


class NodeInformationStatus(Enum):
    """Enum for node information status."""

    OK = 0  # pylint: disable=invalid-name
    Error_Request_Rejected = 1
    Error_Invalid_Node_Index = 2


class FrameGetNodeInformationConfirmation(FrameBase):
    """Frame for confirmation for node information request."""

    def __init__(self, status=NodeInformationStatus.OK, node_id=None):
        """Init Frame."""
        super().__init__(Command.GW_GET_NODE_INFORMATION_CFM)
        self.status = status
        self.node_id = node_id

    def get_payload(self):
        """Return Payload."""
        return bytes([self.status.value, self.node_id])

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.status = NodeInformationStatus(payload[0])
        self.node_id = payload[1]

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetNodeInformationConfirmation node_id={} status=\'{}\'/>'.format(self.node_id, self.status)


class FrameGetNodeInformationNotification(FrameBase):
    """Frame for notification of note information request."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_NODE_INFORMATION_NTF)
        self.node_id = None
        self.order = None
        self.placement = None
        self.name = None
        self.velocity = None

        self._serial_number = bytes(8)

        self.current_position = None
        self.target = None
        self.fp1_current_position = None
        self.fp2_current_position = None
        self.fp3_current_position = None
        self.fp4_current_position = None

    @property
    def serial_number(self):
        """Property for serial number in a human readable way."""
        return ":".join("{:02x}".format(c) for c in self._serial_number)

    def get_payload(self):
        """Return Payload."""
        # ret = bytes([len(self.scenes)])
        # for number, name in self.scenes:
        #    ret += bytes([number])
        #    ret += string_to_bytes(name, 64)
        # ret += bytes([self.remaining_scenes])
        # return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.node_id = payload[0]
        self.order = payload[1] * 256 + payload[2]
        self.placement = payload[3]
        self.name = bytes_to_string(payload[4:68])
        self.velocity = payload[68]
        self._serial_number = payload[75:83]

        print("STATE: ", payload[84-1])

        self.current_position = payload[85-1] * 256 + payload[86-1]
        self.target = payload[87-1] * 256 + payload[88-1]
        self.fp1_current_position = payload[89-1] * 256 + payload[90-1]
        self.fp2_current_position = payload[91-1] * 256 + payload[92-1]
        self.fp3_current_position = payload[93-1] * 256 + payload[94-1]
        self.fp4_current_position = payload[95-1] * 256 + payload[96-1]

    def __str__(self):
        """Return human readable string."""
        def format_position(pos):
            if pos == 0xF7FF:
                return '\'n/a\''
            return pos
        return \
            '<FrameGetNodeInformationNotification ' \
            'node_id={} order={} placement={} name=\'{}\' velocity=\'{}\'' \
            ' serial_number=\'{}\'' \
            ' current_position={}' \
            ' target_position={}' \
            ' fp1_current_position={}' \
            ' fp2_current_position={}' \
            ' fp3_current_position={}' \
            ' fp4_current_position={}' \
            '/>'.format(
                self.node_id, self.order, self.placement, self.name, self.velocity,
                self.serial_number,
                format_position(self.current_position),
                format_position(self.target),
                format_position(self.fp1_current_position),
                format_position(self.fp2_current_position),
                format_position(self.fp3_current_position),
                format_position(self.fp4_current_position))
