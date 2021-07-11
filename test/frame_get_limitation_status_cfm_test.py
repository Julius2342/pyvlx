"""Unit tests for FrameGetLimitationStatusConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames.frame_get_limitation import (
    FrameGetLimitationStatusConfirmation)


class TestFrameGetLimitationStatusConfirmation(unittest.TestCase):
    """Test class for FrameGetLimitationStatusConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameGetLimitationStatusConfirmation bytes."""
        frame = FrameGetLimitationStatusConfirmation(session_id=1, data=1)
        self.assertEqual(bytes(frame), b'\x00\x06\x03\x13\x00\x01\x01\x16')

        frame = FrameGetLimitationStatusConfirmation(session_id=2, data=0)
        self.assertEqual(bytes(frame), b'\x00\x06\x03\x13\x00\x02\x00\x14')

    def test_frame_from_raw(self):
        """Test parse FrameGetLimitationStatusConfirmation from raw."""
        frame = frame_from_raw(b'\x00\x06\x03\x13\x00\x01\x01\x16')
        self.assertTrue(isinstance(frame, FrameGetLimitationStatusConfirmation))
        self.assertEqual(frame.session_id, 1)
        self.assertEqual(frame.data, 1)

        frame = frame_from_raw(b'\x00\x06\x03\x13\x00\x02\x00\x14')
        self.assertTrue(isinstance(frame, FrameGetLimitationStatusConfirmation))
        self.assertEqual(frame.session_id, 2)
        self.assertEqual(frame.data, 0)

    def test_str(self):
        """Test string representation of FrameGetLimitationStatusConfirmation."""
        frame = FrameGetLimitationStatusConfirmation(session_id=1)
        self.assertEqual(str(frame),
                         '<FrameGetLimitationStatusConfirmation session_id="1" status="None"/>')
