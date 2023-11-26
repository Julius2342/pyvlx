"""Unit tests for FrameCommandSendRequest."""
import unittest

from pyvlx import Position, PyVLXException
from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameCommandSendRequest
from pyvlx.const import Originator


class TestFrameCommandSendRequest(unittest.TestCase):
    """Test class FrameCommandSendRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAME = (
        b"\x00E\x03\x00\x03\xe8\x02\x03\x00\x00\x00\x96\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x01\x02"
        + b"\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        + b"\x00\x00\x00\x00\x00\x009"
    )

    def test_bytes(self) -> None:
        """Test FrameCommandSendRequest with NO_TYPE."""
        frame = FrameCommandSendRequest(
            node_ids=[1, 2, 3],
            parameter=Position(position_percent=75),
            session_id=1000,
            originator=Originator.RAIN,
        )
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameCommandSendRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameCommandSendRequest))
        self.assertEqual(frame.node_ids, [1, 2, 3])
        self.assertEqual(Position(frame.parameter).position_percent, 75)
        self.assertEqual(frame.session_id, 1000)
        self.assertEqual(frame.originator, Originator.RAIN)

    def test_str(self) -> None:
        """Test string representation of FrameCommandSendRequest."""
        functional_para = {"fp3": Position(position=12345)}
        functional_parameter = {}
        for i in range(1, 17):
            key = "fp%s" % (i)
            if key in functional_para:
                functional_parameter[key] = functional_para[key]
            else:
                functional_parameter[key] = bytes(2)
        frame = FrameCommandSendRequest(
            node_ids=[1, 2, 3],
            parameter=Position(position=12345),
            **functional_parameter,
            session_id=1000,
            originator=Originator.RAIN
        )
        self.assertEqual(
            str(frame),
            '<FrameCommandSendRequest node_ids="[1, 2, 3]" active_parameter="0" parameter="24 %" '
            'functional_parameter="fp1: 0 %, fp2: 0 %, fp3: 24 %, fp4: 0 %, fp5: 0 %, fp6: 0 %, fp7: 0 %, '
            'fp8: 0 %, fp9: 0 %, fp10: 0 %, fp11: 0 %, fp12: 0 %, fp13: 0 %, fp14: 0 %, fp15: 0 %, fp16: 0 %, " '
            'session_id="1000" originator="Originator.RAIN"/>',
        )

    def test_wrong_payload(self) -> None:
        """Test wrong payload length, 2 scenes in len, only one provided."""
        frame = FrameCommandSendRequest()
        with self.assertRaises(PyVLXException) as ctx:
            frame.from_payload(
                b"\x03\xe8\x01\x03\x00\x00\x0009\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x15\x01\x02\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
                b"\x00\x00\x00\x00\x00\x00\x00"
            )
        self.assertEqual(
            ctx.exception.description, "command_send_request_wrong_node_length"
        )
