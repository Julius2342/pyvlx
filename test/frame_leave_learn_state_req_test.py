"""Unit tests for FrameLeaveLearnStateRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameLeaveLearnStateRequest


class TestFrameLeaveLearnStateRequest(unittest.TestCase):
    """Test class FrameLeaveLearnStateRequest."""

    EXAMPLE_FRAME = b"\x00\x03\x00\x0e\r"

    def test_bytes(self) -> None:
        """Test FrameLeaveLearnStateRequest with NO_TYPE."""
        frame = FrameLeaveLearnStateRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameLeaveLearnStateRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameLeaveLearnStateRequest))

    def test_str(self) -> None:
        """Test string representation of FrameGetStateRequest."""
        frame = FrameLeaveLearnStateRequest()
        self.assertEqual(str(frame), "<FrameLeaveLearnStateRequest/>")
