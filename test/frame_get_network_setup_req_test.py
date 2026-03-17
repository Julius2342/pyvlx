"""Unit tests for FrameGetNetworkSetupRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetNetworkSetupRequest


class TestFrameGetNetworkSetupRequest(unittest.TestCase):
    """Test class for FrameGetNetworkSetupRequest."""

    def test_bytes(self) -> None:
        """Test FrameGetNetworkSetupRequest with NO_TYPE."""
        frame = FrameGetNetworkSetupRequest()
        self.assertEqual(bytes(frame), b"\x00\x03\x00\xe0\xe3")

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetNetworkSetupRequest from raw."""
        frame = frame_from_raw(b"\x00\x03\x00\xe0\xe3")
        self.assertTrue(isinstance(frame, FrameGetNetworkSetupRequest))

    def test_str(self) -> None:
        """Test string representation of FrameGetNetworkSetupRequest."""
        frame = FrameGetNetworkSetupRequest()
        self.assertEqual(str(frame), "<FrameGetNetworkSetupRequest/>")
