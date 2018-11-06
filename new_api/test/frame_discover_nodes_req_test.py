"""Unit tests for FrameDiscoverNodesRequest."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_discover_nodes import FrameDiscoverNodesRequest
from pyvlx.const import NodeType


class TestFrameNodeDiscover(unittest.TestCase):
    """Test class for FrameDiscoverNodesRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_discover_node_request(self):
        """Test FrameDiscoverNodesRequest with NO_TYPE."""
        frame = FrameDiscoverNodesRequest()
        self.assertEqual(bytes(frame), b'\x00\x04\x01\x03\x00\x06')

    def test_discover_node_request_light(self):
        """Test FrameDiscoverNodesRequest with Light."""
        frame = FrameDiscoverNodesRequest(NodeType.LIGHT)
        self.assertEqual(bytes(frame), b'\x00\x04\x01\x03\x06\x00')

    def test_discover_node_request_from_raw(self):
        """Test parse FrameDiscoverNodesRequest from raw."""
        frame = frame_from_raw(b'\x00\x04\x01\x03\x06\x00')
        self.assertTrue(isinstance(frame, FrameDiscoverNodesRequest))
        self.assertEqual(frame.node_type, NodeType.LIGHT)
