"""Unit tests for FrameGetStateRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetStateRequest


class TestFrameGetStateRequest(unittest.TestCase):
    """Test class FrameGetStateRequest."""

    EXAMPLE_FRAME = b"\x00\x03\x00\x0c\x0f"

    def test_bytes(self) -> None:
        """Test FrameGetStateRequest with NO_TYPE."""
        frame = FrameGetStateRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetStateRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetStateRequest))

    def test_str(self) -> None:
        """Test string representation of FrameGetStateRequest."""
        frame = FrameGetStateRequest()
        self.assertEqual(str(frame), "<FrameGetStateRequest/>")
