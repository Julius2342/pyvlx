"""Unit tests for FrameActivationLogUpdatedNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameActivationLogUpdatedNotification


class TestFrameActivationLogUpdatedNotification(unittest.TestCase):
    """Test class for FrameActivationLogUpdatedNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x05\x06\x00"

    def test_bytes(self):
        """Test FrameActivationLogUpdatedNotification with NO_TYPE."""
        frame = FrameActivationLogUpdatedNotification()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameActivationLogUpdatedNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameActivationLogUpdatedNotification))

    def test_str(self):
        """Test string representation of FrameActivationLogUpdatedNotification."""
        frame = FrameActivationLogUpdatedNotification()
        self.assertEqual(str(frame), "<FrameActivationLogUpdatedNotification/>")
