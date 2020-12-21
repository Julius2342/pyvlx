"""Unit tests for FrameCommandRemainingTimeNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameCommandRemainingTimeNotification


class TestFrameCommandRemainingTimeNotification(unittest.TestCase):
    """Test class FrameCommandRemainingTimeNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameCommandRemainingTimeNotification."""
        frame = FrameCommandRemainingTimeNotification(
            session_id=1000, index_id=23, node_parameter=42, seconds=1337
        )
        self.assertEqual(bytes(frame), b"\x00\t\x03\x03\x03\xe8\x17*\x059\xe3")

    def test_frame_from_raw(self):
        """Test parse FrameCommandRemainingTimeNotification from raw."""
        frame = frame_from_raw(b"\x00\t\x03\x03\x03\xe8\x17*\x059\xe3")
        self.assertTrue(isinstance(frame, FrameCommandRemainingTimeNotification))
        self.assertEqual(frame.session_id, 1000)
        self.assertEqual(frame.index_id, 23)
        self.assertEqual(frame.node_parameter, 42)
        self.assertEqual(frame.seconds, 1337)

    def test_str(self):
        """Test string representation of FrameCommandRemainingTimeNotification."""
        frame = FrameCommandRemainingTimeNotification(
            session_id=1000, index_id=23, node_parameter=42, seconds=1337
        )
        self.assertEqual(
            str(frame),
            '<FrameCommandRemainingTimeNotification session_id="1000" index_id="23" node_parameter="42" seconds="1337"/>',
        )
