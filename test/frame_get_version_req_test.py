"""Unit tests for FrameGetVersionRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetVersionRequest


class TestFrameGetVersionRequest(unittest.TestCase):
    """Test class FrameGetVersionRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x00\x08\x0b"

    def test_bytes(self):
        """Test FrameGetVersionRequest with NO_TYPE."""
        frame = FrameGetVersionRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameGetVersionRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetVersionRequest))

    def test_str(self):
        """Test string representation of FrameGetVersionRequest."""
        frame = FrameGetVersionRequest()
        self.assertEqual(str(frame), "<FrameGetVersionRequest/>")
