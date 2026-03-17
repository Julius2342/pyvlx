"""Unit tests for FrameGetProtocolVersionRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetProtocolVersionRequest


class TestFrameGetProtocolVersionRequest(unittest.TestCase):
    """Test class FrameGetProtocolVersionRequest."""

    EXAMPLE_FRAME = b"\x00\x03\x00\n\t"

    def test_bytes(self) -> None:
        """Test FrameGetProtocolVersionRequest with NO_TYPE."""
        frame = FrameGetProtocolVersionRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetProtocolVersionRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetProtocolVersionRequest))

    def test_str(self) -> None:
        """Test string representation of FrameGetProtocolVersionRequest."""
        frame = FrameGetProtocolVersionRequest()
        self.assertEqual(str(frame), "<FrameGetProtocolVersionRequest/>")
