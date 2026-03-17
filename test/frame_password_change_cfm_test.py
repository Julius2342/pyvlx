"""Unit tests for FramePasswordChangeConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FramePasswordChangeConfirmation, PasswordChangeConfirmationStatus)


class TestFramePasswordChangeConfirmation(unittest.TestCase):
    """Test class for FramePasswordChangeConfirmation."""

    def test_bytes(self) -> None:
        """Test FramePasswordChangeConfirmation."""
        frame = FramePasswordChangeConfirmation()
        self.assertEqual(bytes(frame), b"\x00\x040\x03\x007")

    def test_bytes_error(self) -> None:
        """Test failed FramePasswordChangeConfirmation."""
        frame = FramePasswordChangeConfirmation(
            status=PasswordChangeConfirmationStatus.FAILED
        )
        self.assertEqual(bytes(frame), b"\x00\x040\x03\x016")

    def test_frame_from_raw(self) -> None:
        """Test parse FramePasswordChangeConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x040\x03\x016")
        self.assertTrue(isinstance(frame, FramePasswordChangeConfirmation))
        self.assertEqual(frame.status, PasswordChangeConfirmationStatus.FAILED)

    def test_str(self) -> None:
        """Test string representation of FramePasswordChangeConfirmation."""
        frame = FramePasswordChangeConfirmation()
        self.assertEqual(
            str(frame),
            '<FramePasswordChangeConfirmation status="PasswordChangeConfirmationStatus.SUCCESSFUL"/>',
        )
