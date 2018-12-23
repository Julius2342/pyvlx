"""Unit tests for FrameCommandSendRequest."""
import unittest

from pyvlx.frame_creation import frame_from_raw
from pyvlx.frames import FrameCommandSendRequest
from pyvlx import Position
from pyvlx.const import Originator
from pyvlx import PyVLXException


class TestFrameCommandSendRequest(unittest.TestCase):
    """Test class FrameCommandSendRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = \
        b'\x00E\x03\x00\x03\xe8\x02\x03\x00\x00\x00\x96\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x02' \
        + b'\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' \
        + b'\x00\x00\x00\x00\x00\x009'

    def test_bytes(self):
        """Test FrameCommandSendRequest with NO_TYPE."""
        frame = FrameCommandSendRequest(node_ids=[1, 2, 3], parameter=Position(position_percent=75), session_id=1000, originator=Originator.RAIN)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self):
        """Test parse FrameCommandSendRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameCommandSendRequest))
        self.assertEqual(frame.node_ids, [1, 2, 3])
        self.assertEqual(Position(frame.parameter).position_percent, 75)
        self.assertEqual(frame.session_id, 1000)
        self.assertEqual(frame.originator, Originator.RAIN)

    def test_str(self):
        """Test string representation of FrameCommandSendRequest."""
        frame = FrameCommandSendRequest(node_ids=[1, 2, 3], parameter=Position(position=12345), session_id=1000, originator=Originator.RAIN)
        self.assertEqual(
            str(frame),
            '<FrameCommandSendRequest node_ids=[1, 2, 3] parameter="24 %" session_id=1000 originator=Originator.RAIN/>')

    def test_wrong_payload(self):
        """Test wrong payload length, 2 scenes in len, only one provided."""
        frame = FrameCommandSendRequest()
        with self.assertRaises(PyVLXException) as ctx:
            frame.from_payload(
                b'\x03\xe8\x01\x03\x00\x00\x0009\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                b'\x00\x15\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                b'\x00\x00\x00\x00\x00\x00\x00')
        self.assertEqual(ctx.exception.description, 'command_send_request_wrong_node_length')
