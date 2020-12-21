"""Unit tests for FrameDiscoverNodesConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameDiscoverNodesConfirmation


class TestFrameNodeDiscoverConfirmation(unittest.TestCase):
    """Test class for FrameDiscoverNodesConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameDiscoverNodesConfirmation."""
        frame = FrameDiscoverNodesConfirmation()
        self.assertEqual(bytes(frame), b"\x00\x03\x01\x04\x06")

    def test_frame_from_raw(self):
        """Test parse FrameDiscoverNodesConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x03\x01\x04\x06")
        self.assertTrue(isinstance(frame, FrameDiscoverNodesConfirmation))

    def test_str(self):
        """Test string representation of FrameDiscoverNodesConfirmation."""
        frame = FrameDiscoverNodesConfirmation()
        self.assertEqual(str(frame), "<FrameDiscoverNodesConfirmation/>")
