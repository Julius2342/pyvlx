"""Module for requesting change of node name."""

from pyvlx.const import Command, NodeVariation
from pyvlx.string_helper import bytes_to_string, string_to_bytes

from .frame import FrameBase


class FrameNodeInformationChangedNotification(FrameBase):
    """Frame for notification for set node name."""

    PAYLOAD_LEN = 69

    def __init__(
            self,
            node_id: int = 0,
            name: str | None = None,
            order: int = 0,
            placement: int = 0,
            node_variation: NodeVariation = NodeVariation.NOT_SET,
    ):
        """Init Frame."""
        super().__init__(Command.GW_NODE_INFORMATION_CHANGED_NTF)
        self.node_id = node_id
        self.name = name
        self.order = order
        self.placement = placement
        self.node_variation = node_variation

    def get_payload(self) -> bytes:
        """Return Payload."""
        payload = bytes([self.node_id])
        assert self.name is not None
        payload += string_to_bytes(self.name, 64)
        payload += bytes([self.order >> 8 & 255, self.order & 255])
        payload += bytes([self.placement])
        payload += bytes([self.node_variation.value])
        return payload

    def from_payload(self, payload: bytes) -> None:
        """Init frame from binary data."""
        self.node_id = payload[0]
        self.name = bytes_to_string(payload[1:65])
        self.order = payload[65] * 256 + payload[66]
        self.placement = payload[67]
        self.node_variation = NodeVariation(payload[68])

    def __str__(self) -> str:
        """Return human readable string."""
        return (
            f'<{type(self).__name__} node_id="{self.node_id}" name="{self.name}" order="{self.order}" '
            f'placement="{self.placement}" node_variation="{self.node_variation}"/>'
        )
