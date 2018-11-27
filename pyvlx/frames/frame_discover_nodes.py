"""Module for discover nodes requests."""
from pyvlx.const import Command, NodeType

from .frame import FrameBase


class FrameDiscoverNodesRequest(FrameBase):
    """Frame for discover nodes request."""

    PAYLOAD_LEN = 1

    def __init__(self, node_type=NodeType.NO_TYPE):
        """Init Frame."""
        super().__init__(Command.GW_CS_DISCOVER_NODES_REQ)
        self.node_type = node_type

    def get_payload(self):
        """Return Payload."""
        ret = bytes([self.node_type.value])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.node_type = NodeType(payload[0])

    def __str__(self):
        """Return human readable string."""
        return '<FrameDiscoverNodesRequest node_type=\'{}\'/>'.format(self.node_type)


class FrameDiscoverNodesConfirmation(FrameBase):
    """Frame for discover nodes confirmation."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_CS_DISCOVER_NODES_CFM)


class FrameDiscoverNodesNotification(FrameBase):
    """Frame for discover nodes notification."""

    PAYLOAD_LEN = 131

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_CS_DISCOVER_NODES_NTF)
        self.payload = b'\0' * 131

    def get_payload(self):
        """Return Payload."""
        return self.payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.payload = payload

    def __str__(self):
        """Return human readable string."""
        return '<FrameDiscoverNodesNotification payload=\'{}\'/>'.format(":".join("{:02x}".format(c) for c in self.payload))
