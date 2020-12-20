"""Unit tests for FrameHouseStatusMonitorEnableConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameHouseStatusMonitorEnableConfirmation


class TestFrameHouseStatusMonitorEnableConfirmation(unittest.TestCase):
    """Test class FrameHouseStatusMonitorEnableConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x02A@"

    def test_bytes(self):
        """Test FrameHouseStatusMonitorEnableConfirmation."""
        frame = FrameHouseStatusMonitorEnableConfirmation()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameHouseStatusMonitorEnableConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameHouseStatusMonitorEnableConfirmation))

    def test_str(self):
        """Test string representation of FrameHouseStatusMonitorEnableConfirmation."""
        frame = FrameHouseStatusMonitorEnableConfirmation()
        self.assertEqual(str(frame), "<FrameHouseStatusMonitorEnableConfirmation/>")
