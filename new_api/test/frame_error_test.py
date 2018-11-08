"""Unit tests for FrameErrorNotification."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_error_notification import FrameErrorNotification, ErrorType


class TestErrorNotification(unittest.TestCase):
    """Test class for FrameErrorNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_error_notification(self):
        """Test FrameErrorNotification with Light."""
        frame = FrameErrorNotification(error_type=ErrorType.ErrorOnFrameStructure)
        self.assertEqual(bytes(frame), b'\x00\x04\x00\x00\x02\x06')

    def test_error_notification_from_raw(self):
        """Test parse FrameErrorNotification from raw."""
        frame = frame_from_raw(b'\x00\x04\x00\x00\x02\x06')
        self.assertTrue(isinstance(frame, FrameErrorNotification))
        self.assertEqual(frame.error_type, ErrorType.ErrorOnFrameStructure)

    def test_str(self):
        """Test string representation of FrameErrorNotification."""
        frame = FrameErrorNotification(error_type=ErrorType.ErrorOnFrameStructure)
        self.assertEqual(
            str(frame),
            '<FrameErrorNotification error_type=\'ErrorType.ErrorOnFrameStructure\'/>')
