"""Unit tests for FrameGetLocalTimeRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetLocalTimeRequest


class TestFrameGetLocalTimeRequest(unittest.TestCase):
    """Test class for FrameGetLocalTimeRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetLocalTimeRequest with NO_TYPE."""
        frame = FrameGetLocalTimeRequest()
        self.assertEqual(bytes(frame), b"\x00\x03\x20\x04\x27")

    def test_frame_from_raw(self):
        """Test parse FrameGetLocalTimeRequest from raw."""
        frame = frame_from_raw(b"\x00\x03\x20\x04\x27")
        self.assertTrue(isinstance(frame, FrameGetLocalTimeRequest))

    def test_str(self):
        """Test string representation of FrameGetLocalTimeRequest."""
        frame = FrameGetLocalTimeRequest()
        self.assertEqual(str(frame), "<FrameGetLocalTimeRequest/>")
