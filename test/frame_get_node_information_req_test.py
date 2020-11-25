"""Unit tests for FrameGetNodeInformationRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetNodeInformationRequest


class TestFrameGetNodeInformationRequest(unittest.TestCase):
    """Test class for FrameGetNodeInformationRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetNodeInformationRequest with NO_TYPE."""
        frame = FrameGetNodeInformationRequest(node_id=23)
        self.assertEqual(bytes(frame), b"\x00\x04\x02\x00\x17\x11")

    def test_frame_from_raw(self):
        """Test parse FrameGetNodeInformationRequest from raw."""
        frame = frame_from_raw(b"\x00\x04\x02\x00\x17\x11")
        self.assertTrue(isinstance(frame, FrameGetNodeInformationRequest))
        self.assertEqual(frame.node_id, 23)

    def test_str(self):
        """Test string representation of FrameGetNodeInformationRequest."""
        frame = FrameGetNodeInformationRequest(node_id=23)
        self.assertEqual(str(frame), '<FrameGetNodeInformationRequest node_id="23"/>')
