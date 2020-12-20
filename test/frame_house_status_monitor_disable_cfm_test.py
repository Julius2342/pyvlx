"""Unit tests for FrameHouseStatusMonitorDisableConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameHouseStatusMonitorDisableConfirmation


class TestFrameHouseStatusMonitorDisableConfirmation(unittest.TestCase):
    """Test class FrameHouseStatusMonitorDisableConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x02CB"

    def test_bytes(self):
        """Test FrameHouseStatusMonitorDisableConfirmation."""
        frame = FrameHouseStatusMonitorDisableConfirmation()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameHouseStatusMonitorDisableConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameHouseStatusMonitorDisableConfirmation))

    def test_str(self):
        """Test string representation of FrameHouseStatusMonitorDisableConfirmation."""
        frame = FrameHouseStatusMonitorDisableConfirmation()
        self.assertEqual(str(frame), "<FrameHouseStatusMonitorDisableConfirmation/>")
