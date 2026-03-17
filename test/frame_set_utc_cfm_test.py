"""Unit tests for FrameSetUTCConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameSetUTCConfirmation


class TestFrameSetUTCConfirmation(unittest.TestCase):
    """Test class FrameSetUTCConfirmation."""

    EXAMPLE_FRAME = b'\x00\x03 \x01"'

    def test_bytes(self) -> None:
        """Test FrameSetUTCConfirmation."""
        frame = FrameSetUTCConfirmation()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameSetUTCConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameSetUTCConfirmation))

    def test_str(self) -> None:
        """Test string representation of FrameSetUTCConfirmation."""
        frame = FrameSetUTCConfirmation()
        self.assertEqual(str(frame), "<FrameSetUTCConfirmation/>")
