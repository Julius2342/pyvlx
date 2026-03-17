"""Unit tests for FrameGetProtocolVersionConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetProtocolVersionConfirmation


class TestFrameGetProtocolVersionConfirmation(unittest.TestCase):
    """Test class for FrameGetProtocolVersionConfirmation."""

    EXAMPLE_FRAME = b"\x00\x07\x00\x0b\x04\xd2\x10\xe1+"

    def test_bytes(self) -> None:
        """Test FrameGetProtocolVersionConfirmation."""
        frame = FrameGetProtocolVersionConfirmation(
            major_version=1234, minor_version=4321
        )
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetProtocolVersionConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameGetProtocolVersionConfirmation))
        self.assertEqual(frame.major_version, 1234)
        self.assertEqual(frame.minor_version, 4321)

    def test_str(self) -> None:
        """Test string representation of FrameGetProtocolVersionConfirmation."""
        frame = FrameGetProtocolVersionConfirmation(
            major_version=1234, minor_version=4321
        )
        self.assertEqual(
            str(frame), '<FrameGetProtocolVersionConfirmation version="1234.4321"/>'
        )
