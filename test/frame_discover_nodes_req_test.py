"""Unit tests for FrameDiscoverNodesRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameDiscoverNodesRequest
from pyvlx.const import NodeType


class TestFrameNodeDiscover(unittest.TestCase):
    """Test class for FrameDiscoverNodesRequest."""

    def test_bytes(self) -> None:
        """Test FrameDiscoverNodesRequest with NO_TYPE."""
        frame = FrameDiscoverNodesRequest()
        self.assertEqual(bytes(frame), b"\x00\x04\x01\x03\x00\x06")

    def test_bytes_light(self) -> None:
        """Test FrameDiscoverNodesRequest with Light."""
        frame = FrameDiscoverNodesRequest(NodeType.LIGHT)
        self.assertEqual(bytes(frame), b"\x00\x04\x01\x03\x06\x00")

    def test_frame_from_raw(self) -> None:
        """Test parse FrameDiscoverNodesRequest from raw."""
        frame = frame_from_raw(b"\x00\x04\x01\x03\x06\x00")
        self.assertTrue(isinstance(frame, FrameDiscoverNodesRequest))
        self.assertEqual(frame.node_type, NodeType.LIGHT)

    def test_str(self) -> None:
        """Test string representation of FrameDiscoverNodesRequest."""
        frame = FrameDiscoverNodesRequest(NodeType.LIGHT)
        self.assertEqual(
            str(frame), '<FrameDiscoverNodesRequest node_type="NodeType.LIGHT"/>'
        )
