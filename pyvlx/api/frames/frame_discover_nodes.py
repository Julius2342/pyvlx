"""Module for discover nodes requests."""
from ...const import Command, NodeType, DiscoverStatus

from .frame import FrameBase

from ...string_helper import (statusflags_from_bytes, bytes_from_statusflags)


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
        return '<{} node_type="{}"/>'.format(type(self).__name__, self.node_type)


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
        self.addednodes = []
        self.rfconnectionerror = []
        self.iokeyerrorexistingnode = []
        self.removed = []
        self.open = []
        self.discoverstatus = DiscoverStatus.OK
        self.payload = self.get_payload()

    def get_payload(self):
        """Return Payload."""
        payload = bytes_from_statusflags(self.addednodes, 26)
        payload += bytes_from_statusflags(self.rfconnectionerror, 26)
        payload += bytes_from_statusflags(self.iokeyerrorexistingnode, 26)
        payload += bytes_from_statusflags(self.removed, 26)
        payload += bytes_from_statusflags(self.open, 26)
        payload += bytes([self.discoverstatus.value])
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.addednodes = statusflags_from_bytes(payload[:26])
        self.rfconnectionerror = statusflags_from_bytes(payload[26:53])
        self.iokeyerrorexistingnode = statusflags_from_bytes(payload[53:79])
        self.removed = statusflags_from_bytes(payload[79:105])
        self.open = statusflags_from_bytes(payload[105:131])
        self.discoverstatus = DiscoverStatus(payload[130])

    def __str__(self):
        """Return human readable string."""
        return ('<{} addednodes="{}" rfconnectionerror="{}" iokeyerrorexistingnode="{}"'
                'removed="{}" open="{}" discoverstatus="{}"/>'.format(
                    type(self).__name__,
                    self.addednodes,
                    self.rfconnectionerror,
                    self.iokeyerrorexistingnode,
                    self.removed,
                    self.open,
                    self.discoverstatus))
