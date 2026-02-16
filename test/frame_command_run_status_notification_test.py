"""Unit tests for FrameCommandRunStatusNotification."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import FrameCommandRunStatusNotification
from pyvlx.const import RunStatus, StatusReply


class TestFrameCommandRunStatusNotification(unittest.TestCase):
    """Test class FrameCommandRunStatusNotification."""

    # pylint: disable=too-many-public-methods,invalid-name

    EXAMPLE_FRAMES = [
        (
            "execution_completed",
            b"\x00\x10\x03\x02\x03\xe8\x07\x17*\x059\x00\xee\x00\x00\x00\x00\x12",
            RunStatus.EXECUTION_COMPLETED,
            StatusReply.LIMITATION_BY_EMERGENCY,
        ),
        (
            "execution_active",
            b"\x00\x10\x03\x02\x03\xe8\x07\x17*\x059\x02\xe2\x00\x00\x00\x00\x1c",
            RunStatus.EXECUTION_ACTIVE,
            StatusReply.LIMITATION_BY_USER,
        ),
        (
            "execution_failed",
            b"\x00\x10\x03\x02\x03\xe8\x07\x17*\x059\x01\xe3\x00\x00\x00\x00\x1e",
            RunStatus.EXECUTION_FAILED,
            StatusReply.LIMITATION_BY_RAIN,
        ),
    ]

    def test_bytes(self):
        """Test FrameCommandRunStatusNotification."""
        for name, raw, run_status, status_reply in self.EXAMPLE_FRAMES:
            with self.subTest(name=name):
                frame = FrameCommandRunStatusNotification(
                    session_id=1000,
                    status_id=7,
                    index_id=23,
                    node_parameter=42,
                    parameter_value=1337,
                    run_status=run_status,
                    status_reply=status_reply,
                )
                self.assertEqual(bytes(frame), raw)

    def test_frame_from_raw(self):
        """Test parse FrameCommandRunStatusNotification from raw."""
        for name, raw, run_status, status_reply in self.EXAMPLE_FRAMES:
            with self.subTest(name=name):
                frame = frame_from_raw(raw)
                self.assertIsInstance(frame, FrameCommandRunStatusNotification)
                self.assertEqual(frame.session_id, 1000)
                self.assertEqual(frame.status_id, 7)
                self.assertEqual(frame.index_id, 23)
                self.assertEqual(frame.node_parameter, 42)
                self.assertEqual(frame.parameter_value, 1337)
                self.assertEqual(frame.run_status, run_status)
                self.assertEqual(frame.status_reply, status_reply)

    def test_str(self):
        """Test string representation of FrameCommandRunStatusNotification."""
        frame = FrameCommandRunStatusNotification(
            session_id=1000,
            status_id=7,
            index_id=23,
            node_parameter=42,
            parameter_value=1337,
            run_status=RunStatus.EXECUTION_FAILED,
            status_reply=StatusReply.LIMITATION_BY_RAIN,
        )
        self.assertEqual(
            str(frame),
            '<FrameCommandRunStatusNotification session_id="1000" status_id="7" index_id="23" node_parameter="42" '
            'parameter_value="1337" run_status="RunStatus.EXECUTION_FAILED" '
            'status_reply="StatusReply.LIMITATION_BY_RAIN"/>',
        )
