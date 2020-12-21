"""Unit tests for FrameLeaveLearnStateRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameLeaveLearnStateRequest


class TestFrameLeaveLearnStateRequest(unittest.TestCase):
    """Test class FrameLeaveLearnStateRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x00\x0e\r"

    def test_bytes(self):
        """Test FrameLeaveLearnStateRequest with NO_TYPE."""
        frame = FrameLeaveLearnStateRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameLeaveLearnStateRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameLeaveLearnStateRequest))

    def test_str(self):
        """Test string representation of FrameGetStateRequest."""
        frame = FrameLeaveLearnStateRequest()
        self.assertEqual(str(frame), "<FrameLeaveLearnStateRequest/>")
