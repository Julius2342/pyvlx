"""Unit tests for FrameHouseStatusMonitorEnableRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameHouseStatusMonitorEnableRequest


class TestFrameHouseStatusMonitorEnableRequest(unittest.TestCase):
    """Test class FrameHouseStatusMonitorEnableRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = b"\x00\x03\x02@A"

    def test_bytes(self):
        """Test FrameHouseStatusMonitorEnableRequest."""
        frame = FrameHouseStatusMonitorEnableRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameHouseStatusMonitorEnableRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameHouseStatusMonitorEnableRequest))

    def test_str(self):
        """Test string representation of FrameHouseStatusMonitorEnableRequest."""
        frame = FrameHouseStatusMonitorEnableRequest()
        self.assertEqual(str(frame), "<FrameHouseStatusMonitorEnableRequest/>")
