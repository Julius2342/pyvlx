"""Unit tests for FrameGetLocalTimeConfirmation."""
import unittest
from datetime import datetime, timezone

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameGetLocalTimeConfirmation


class TestFrameGetLocalTimeConfirmation(unittest.TestCase):
    """Test class for FrameGetLocalTimeConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self) -> None:
        """Test FrameGetLocalTimeConfirmation."""
        frame = FrameGetLocalTimeConfirmation()
        frame.time.localtime = datetime(2020, 12, 3, 18, 19, 19, 176900)
        frame.time.utctime = datetime(
            2020, 12, 3, 18, 19, 19, 176900, tzinfo=timezone.utc
        )
        self.assertEqual(
            bytes(frame), b"\x00\x12 \x05_\xc9,'\x13\x13\x12\x03\x0c\x00x\x04\x01R\xffg"
        )

    def test_frame_from_raw(self) -> None:
        """Test parse FrameGetLocalTimeConfirmation from raw."""
        frame = frame_from_raw(
            b"\x00\x12 \x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x007"
        )
        self.assertTrue(isinstance(frame, FrameGetLocalTimeConfirmation))

    def test_str(self) -> None:
        """Test string representation of FrameGetLocalTimeConfirmation."""
        frame = FrameGetLocalTimeConfirmation()
        frame.time.localtime = datetime.strptime(
            "2020-12-03 18:19:19.176900", "%Y-%m-%d %H:%M:%S.%f"
        )
        frame.time.utctime = datetime.strptime(
            "2020-12-03 18:19:19.176900", "%Y-%m-%d %H:%M:%S.%f"
        )
        self.assertEqual(
            str(frame),
            "<FrameGetLocalTimeConfirmation><DtoLocalTime "
            'utctime="2020-12-03 18:19:19.176900" '
            'localtime="2020-12-03 18:19:19.176900"/>'
            "</FrameGetLocalTimeConfirmation>",
        )
