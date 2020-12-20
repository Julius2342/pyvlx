"""Unit tests for FrameGetSystemTableDataRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetSystemTableDataRequest


class TestFrameGetSystemTableDataRequest(unittest.TestCase):
    """Test class for FrameGetSystemTableDataRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetSystemTableDataRequest with NO_TYPE."""
        frame = FrameGetSystemTableDataRequest()
        self.assertEqual(bytes(frame), b'\x00\x03\x01\x00\x02')

    def test_frame_from_raw(self):
        """Test parse FrameGetSystemTableDataRequest from raw."""
        frame = frame_from_raw(b'\x00\x03\x01\x00\x02')
        self.assertTrue(isinstance(frame, FrameGetSystemTableDataRequest))

    def test_str(self):
        """Test string representation of FrameGetSystemTableDataRequest."""
        frame = FrameGetSystemTableDataRequest()
        self.assertEqual(str(frame), "<FrameGetSystemTableDataRequest/>")
