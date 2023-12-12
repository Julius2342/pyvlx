"""Unit tests for FrameLeaveLearnStateConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameLeaveLearnStateConfirmation


class TestFrameLeaveLearnStateConfirmation(unittest.TestCase):
    """Test class FrameLeaveLearnStateConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x04\x00\x0f\x00\x0b"

    def test_bytes(self) -> None:
        """Test FrameLeaveLearnStateConfirmation."""
        frame = FrameLeaveLearnStateConfirmation()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameLeaveLearnStateConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameLeaveLearnStateConfirmation))

    def test_str(self) -> None:
        """Test string representation of FrameLeaveLearnStateConfirmation."""
        frame = FrameLeaveLearnStateConfirmation()
        self.assertEqual(str(frame), '<FrameLeaveLearnStateConfirmation status="LeaveLearnStateConfirmationStatus.FAILED"/>')
