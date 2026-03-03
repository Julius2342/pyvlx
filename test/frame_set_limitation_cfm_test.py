"""Unit tests for FrameGetLimitationStatusConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames.frame_set_limitation import (
    FrameSetLimitationConfirmation, SetLimitationRequestStatus)


class TestFrameSetLimitationConfirmation(unittest.TestCase):
    """Test class for FrameSetLimitationConfirmation."""

    EXAMPLE_FRAME_ACCEPTED = b'\x00\x06\x03\x11\x00\x01\x01\x14'
    EXAMPLE_FRAME_REJECTED = b'\x00\x06\x03\x11\x00\x02\x00\x16'

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameSetLimitationConfirmation bytes."""
        frame = FrameSetLimitationConfirmation(session_id=1, status=SetLimitationRequestStatus.ACCEPTED)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME_ACCEPTED)

        frame = FrameSetLimitationConfirmation(session_id=2, status=SetLimitationRequestStatus.REJECTED)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME_REJECTED)

    def test_frame_from_raw(self):
        """Test parse FrameGetLimitationStatusConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME_ACCEPTED)
        self.assertTrue(isinstance(frame, FrameSetLimitationConfirmation))
        self.assertEqual(frame.session_id, 1)
        self.assertEqual(frame.status, SetLimitationRequestStatus.ACCEPTED)

        frame = frame_from_raw(self.EXAMPLE_FRAME_REJECTED)
        self.assertTrue(isinstance(frame, FrameSetLimitationConfirmation))
        self.assertEqual(frame.session_id, 2)
        self.assertEqual(frame.status, SetLimitationRequestStatus.REJECTED)

    def test_str(self):
        """Test string representation of FrameSetLimitationConfirmation."""
        frame = FrameSetLimitationConfirmation(session_id=1)
        self.assertEqual(str(frame),
                         '<FrameSetLimitationConfirmation session_id="1" status="None"/>')
