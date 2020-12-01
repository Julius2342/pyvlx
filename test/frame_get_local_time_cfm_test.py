"""Unit tests for FrameGetLocalTimeConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetLocalTimeConfirmation


class TestFrameGetLocalTimeConfirmation(unittest.TestCase):
    """Test class for FrameGetLocalTimeConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetLocalTimeConfirmation."""
        frame = FrameGetLocalTimeConfirmation()
        self.assertEqual(bytes(frame), b"\x00\x12 \x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x007")

    def test_frame_from_raw(self):
        """Test parse FrameGetLocalTimeConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x12 \x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x007")
        self.assertTrue(isinstance(frame, FrameGetLocalTimeConfirmation))

    def test_str(self):
        """Test string representation of FrameGetLocalTimeConfirmation."""
        frame = FrameGetLocalTimeConfirmation()

        self.assertEqual(str(frame), '<FrameGetLocalTimeConfirmation utctime="0" second="0" minute="0" hour="0" dayofmonth="0" '
                         'month="0" year="0" weekday="0" dayofyear="0" daylightsavingflag="0"/>')
