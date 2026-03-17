"""Unit tests for FrameErrorNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import ErrorType, FrameErrorNotification


class TestErrorNotification(unittest.TestCase):
    """Test class for FrameErrorNotification."""

    def test_bytes(self) -> None:
        """Test FrameErrorNotification with Light."""
        frame = FrameErrorNotification(error_type=ErrorType.ErrorOnFrameStructure)
        self.assertEqual(bytes(frame), b"\x00\x04\x00\x00\x02\x06")

    def test_frame_from_raw(self) -> None:
        """Test parse FrameErrorNotification from raw."""
        frame = frame_from_raw(b"\x00\x04\x00\x00\x02\x06")
        self.assertTrue(isinstance(frame, FrameErrorNotification))
        self.assertEqual(frame.error_type, ErrorType.ErrorOnFrameStructure)

    def test_str(self) -> None:
        """Test string representation of FrameErrorNotification."""
        frame = FrameErrorNotification(error_type=ErrorType.ErrorOnFrameStructure)
        self.assertEqual(
            str(frame),
            '<FrameErrorNotification error_type="ErrorType.ErrorOnFrameStructure"/>',
        )
