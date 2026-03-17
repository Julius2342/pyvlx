"""Unit tests for FramePasswordEnterConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FramePasswordEnterConfirmation, PasswordEnterConfirmationStatus)


class TestFramePasswordEnterConfirmation(unittest.TestCase):
    """Test class for FramePasswordEnterConfirmation."""

    def test_bytes(self) -> None:
        """Test FramePasswordEnterConfirmation."""
        frame = FramePasswordEnterConfirmation()
        self.assertEqual(bytes(frame), b"\x00\x040\x01\x005")

    def test_bytes_error(self) -> None:
        """Test failed FramePasswordEnterConfirmation."""
        frame = FramePasswordEnterConfirmation(
            status=PasswordEnterConfirmationStatus.FAILED
        )
        self.assertEqual(bytes(frame), b"\x00\x040\x01\x014")

    def test_frame_from_raw(self) -> None:
        """Test parse FramePasswordEnterConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x040\x01\x014")
        self.assertTrue(isinstance(frame, FramePasswordEnterConfirmation))
        self.assertEqual(frame.status, PasswordEnterConfirmationStatus.FAILED)

    def test_str(self) -> None:
        """Test string representation of FramePasswordEnterConfirmation."""
        frame = FramePasswordEnterConfirmation()
        self.assertEqual(
            str(frame),
            '<FramePasswordEnterConfirmation status="PasswordEnterConfirmationStatus.SUCCESSFUL"/>',
        )
