"""Unit tests for PyVLX Frames."""
import unittest
from pyvlx.frame_discover_nodes import FrameDiscoverNodesConfirmation
from pyvlx.frame_creation import frame_from_raw


class TestFrameNodeDiscoverConfirmation(unittest.TestCase):
    """Test class for PyVLX Frames."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_discover_node_request(self):
        """Test FrameDiscoverNodesConfirmation."""
        frame = FrameDiscoverNodesConfirmation()
        self.assertEqual(bytes(frame), b'\x00\x03\x01\x04\x06')

    def test_discover_node_request_from_raw(self):
        """Test parse FrameDiscoverNodesConfirmation from raw."""
        frame = frame_from_raw(b'\x00\x03\x01\x04\x06')
        self.assertTrue(isinstance(frame, FrameDiscoverNodesConfirmation))
