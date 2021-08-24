"""Unit tests for FrameDiscoverNodesRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameDiscoverNodesRequest
from pyvlx.const import NodeType


class TestFrameNodeDiscover(unittest.TestCase):
    """Test class for FrameDiscoverNodesRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameDiscoverNodesRequest with NO_TYPE."""
        frame = FrameDiscoverNodesRequest()
        self.assertEqual(bytes(frame), b"\x00\x04\x01\x03\x00\x06")

    def test_bytes_light(self):
        """Test FrameDiscoverNodesRequest with Light."""
        frame = FrameDiscoverNodesRequest(NodeType.LIGHT)
        self.assertEqual(bytes(frame), b"\x00\x04\x01\x03\x06\x00")

    def test_frame_from_raw(self):
        """Test parse FrameDiscoverNodesRequest from raw."""
        frame = frame_from_raw(b"\x00\x04\x01\x03\x06\x00")
        self.assertTrue(isinstance(frame, FrameDiscoverNodesRequest))
        self.assertEqual(frame.node_type, NodeType.LIGHT)

    def test_str(self):
        """Test string representation of FrameDiscoverNodesRequest."""
        frame = FrameDiscoverNodesRequest(NodeType.LIGHT)
        self.assertEqual(
            str(frame), '<FrameDiscoverNodesRequest node_type="NodeType.LIGHT"/>'
        )
