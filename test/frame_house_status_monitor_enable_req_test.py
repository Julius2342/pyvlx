"""Unit tests for FrameHouseStatusMonitorEnableRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameHouseStatusMonitorEnableRequest


class TestFrameHouseStatusMonitorEnableRequest(unittest.TestCase):
    """Test class FrameHouseStatusMonitorEnableRequest."""

    EXAMPLE_FRAME = b"\x00\x03\x02@A"

    def test_bytes(self) -> None:
        """Test FrameHouseStatusMonitorEnableRequest."""
        frame = FrameHouseStatusMonitorEnableRequest()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameHouseStatusMonitorEnableRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameHouseStatusMonitorEnableRequest))

    def test_str(self) -> None:
        """Test string representation of FrameHouseStatusMonitorEnableRequest."""
        frame = FrameHouseStatusMonitorEnableRequest()
        self.assertEqual(str(frame), "<FrameHouseStatusMonitorEnableRequest/>")
