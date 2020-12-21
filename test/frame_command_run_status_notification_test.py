"""Unit tests for FrameCommandRunStatusNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameCommandRunStatusNotification


class TestFrameCommandRunStatusNotification(unittest.TestCase):
    """Test class FrameCommandRunStatusNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = (
        b"\x00\x10\x03\x02\x03\xe8\x07\x17*\x059\x00\x00\x00\x00\x00\x00\xfc"
    )

    def test_bytes(self):
        """Test FrameCommandRunStatusNotification."""
        frame = FrameCommandRunStatusNotification(
            session_id=1000,
            status_id=7,
            index_id=23,
            node_parameter=42,
            parameter_value=1337,
        )
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameCommandRunStatusNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameCommandRunStatusNotification))
        self.assertEqual(frame.session_id, 1000)
        self.assertEqual(frame.status_id, 7)
        self.assertEqual(frame.index_id, 23)
        self.assertEqual(frame.node_parameter, 42)
        self.assertEqual(frame.parameter_value, 1337)

    def test_str(self):
        """Test string representation of FrameCommandRunStatusNotification."""
        frame = FrameCommandRunStatusNotification(
            session_id=1000,
            status_id=7,
            index_id=23,
            node_parameter=42,
            parameter_value=1337,
        )
        self.assertEqual(
            str(frame),
            '<FrameCommandRunStatusNotification session_id="1000" status_id="7" index_id="23" node_parameter="42" parameter_value="1337"/>',
        )
