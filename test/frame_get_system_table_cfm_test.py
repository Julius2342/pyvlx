"""Unit tests for FrameGetSystemTableDataConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetSystemTableDataConfirmation


class TestFrameGetSystemTableDataConfirmation(unittest.TestCase):
    """Test class for FrameGetSystemTableDataConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetSystemTableDataConfirmation with NO_TYPE."""
        frame = FrameGetSystemTableDataConfirmation()
        self.assertEqual(bytes(frame), b'\x00\x03\x01\x01\x03')

    def test_frame_from_raw(self):
        """Test parse FrameGetSystemTableDataConfirmation from raw."""
        frame = frame_from_raw(b'\x00\x03\x01\x01\x03')
        self.assertTrue(isinstance(frame, FrameGetSystemTableDataConfirmation))

    def test_str(self):
        """Test string representation of FrameGetSystemTableDataConfirmation."""
        frame = FrameGetSystemTableDataConfirmation()
        self.assertEqual(str(frame), "<FrameGetSystemTableDataConfirmation/>")
