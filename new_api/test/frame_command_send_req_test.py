"""Unit tests for FrameCommandSendRequest."""
import unittest
from pyvlx.frame_creation import frame_from_raw
from pyvlx.frame_command_send import FrameCommandSendRequest


class TestFrameCommandSendRequest(unittest.TestCase):
    """Test class FrameCommandSendRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_command_send_request(self):
        """Test FrameCommandSendRequest with NO_TYPE."""
        frame = FrameCommandSendRequest(node_ids=[1, 2, 3], position=75, session_id=1000)
        self.assertEqual(
            bytes(frame),
            b'\x00E\x03\x00\x03\xe8\x01\x03\x00\x00\x00\x96\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x02'
            + b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00:')

    def test_command_send_request_from_raw(self):
        """Test parse FrameCommandSendRequest from raw."""
        frame = frame_from_raw(
            b'\x00E\x03\x00\x03\xe8\x01\x03\x00\x00\x00\x96\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x02'
            + b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            + b'\x00\x00\x00\x00\x00\x00:')
        self.assertTrue(isinstance(frame, FrameCommandSendRequest))
        self.assertEqual(frame.node_ids, [1, 2, 3])
        self.assertEqual(frame.position, 75)
        self.assertEqual(frame.session_id, 1000)
