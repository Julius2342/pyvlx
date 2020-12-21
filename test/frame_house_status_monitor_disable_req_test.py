"""Unit tests for FrameHouseStatusMonitorDisableRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameHouseStatusMonitorDisableRequest


class TestFrameHouseStatusMonitorDisableRequest(unittest.TestCase):
    """Test class FrameHouseStatusMonitorDisableRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x02BC"

    def test_bytes(self):
        """Test FrameHouseStatusMonitorDisableRequest."""
        frame = FrameHouseStatusMonitorDisableRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameHouseStatusMonitorDisableRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameHouseStatusMonitorDisableRequest))

    def test_str(self):
        """Test string representation of FrameHouseStatusMonitorDisableRequest."""
        frame = FrameHouseStatusMonitorDisableRequest()
        self.assertEqual(str(frame), "<FrameHouseStatusMonitorDisableRequest/>")
