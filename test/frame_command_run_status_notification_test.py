"""Unit tests for FrameCommandRunStatusNotification."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_command_send import FrameCommandRunStatusNotification


class TestFrameCommandRunStatusNotification(unittest.TestCase):
    """Test class FrameCommandRunStatusNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_discover_node_request(self):
        """Test FrameCommandRunStatusNotification."""
        frame = FrameCommandRunStatusNotification(session_id=1000, status_id=7, index_id=23, node_parameter=42, parameter_value=1337)
        self.assertEqual(bytes(frame), b'\x00\n\x03\x02\x03\xe8\x07\x17*\x059\xe6')

    def test_discover_node_request_from_raw(self):
        """Test parse FrameCommandRunStatusNotification from raw."""
        frame = frame_from_raw(b'\x00\n\x03\x02\x03\xe8\x07\x17*\x059\xe6')
        self.assertTrue(isinstance(frame, FrameCommandRunStatusNotification))
        self.assertEqual(frame.session_id, 1000)
        self.assertEqual(frame.status_id, 7)
        self.assertEqual(frame.index_id, 23)
        self.assertEqual(frame.node_parameter, 42)
        self.assertEqual(frame.parameter_value, 1337)

    def test_str(self):
        """Test string representation of FrameCommandRunStatusNotification."""
        frame = FrameCommandRunStatusNotification(session_id=1000, status_id=7, index_id=23, node_parameter=42, parameter_value=1337)
        self.assertEqual(
            str(frame),
            '<FrameCommandRunStatusNotification session_id=1000 status_id=7 index_id=23 node_parameter=42 parameter_value=1337/>')
