"""Unit tests for FrameSetUTCRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameStatusRequestConfirmation, FrameStatusRequestRequest)
from pyvlx.api.frames.frame_status_request import (
    FrameStatusRequestNotification, StatusRequestStatus)
from pyvlx.const import RunStatus, StatusReply, StatusType
from pyvlx.parameter import Parameter


class TestFrameStatusRequestRequest(unittest.TestCase):
    """Test class FrameStatusRequestRequest."""

    EXAMPLE_FRAME = b"\x00\x1d\x03\x05\x00\xab\x02\x01\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                    b"\x00\x00\x00\x00\x01\xfe\x00N"

    def test_bytes(self) -> None:
        """Test FrameStatusRequestRequest with nodes 1,2 and session_id 0xAB."""
        frame = FrameStatusRequestRequest(node_ids=[1, 2], session_id=0xAB)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameStatusRequestRequest from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameStatusRequestRequest))

    def test_str(self) -> None:
        """Test string representation of FrameStatusRequestRequest."""
        frame = FrameStatusRequestRequest(node_ids=[1, 2], session_id=0xAB)
        self.assertEqual(str(frame), "<FrameStatusRequestRequest session_id=\"171\" node_ids=\"[1, 2]\" "
                                     "status_type=\"StatusType.REQUEST_CURRENT_POSITION\" fpi1=\"254\" fpi2=\"0\"/>")


class TestFrameStatusRequestConfirmation(unittest.TestCase):
    """Test class FrameStatusRequestConfirmation."""

    EXAMPLE_FRAME = b"\x00\x06\x03\x06\x00\xab\x01\xa9"

    def test_bytes(self) -> None:
        """Test FrameStatusRequestConfirmation with session_id 0xAB and status ACCEPTED."""
        frame = FrameStatusRequestConfirmation(session_id=0xAB, status=StatusRequestStatus.ACCEPTED)
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameStatusRequestConfirmation from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME)
        self.assertTrue(isinstance(frame, FrameStatusRequestConfirmation))

    def test_str(self) -> None:
        """Test string representation of FrameStatusRequestConfirmation."""
        frame = FrameStatusRequestConfirmation(session_id=0xAB, status=StatusRequestStatus.ACCEPTED)
        self.assertEqual(str(frame),
                         "<FrameStatusRequestConfirmation session_id=\"171\" status=\"StatusRequestStatus.ACCEPTED\"/>")


class TestFrameStatusRequestNotification(unittest.TestCase):
    """Test class FrameStatusRequestNotification."""

    EXAMPLE_FRAME_EMPTY = b"\x00>\x03\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                          b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                          b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00:"
    EXAMPLE_FRAME = b"\x00>\x03\x07\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
                    b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00: "

    def test_bytes(self) -> None:
        """Test FrameStatusRequestNotification."""
        frame = FrameStatusRequestNotification()
        self.assertEqual(bytes(frame), self.EXAMPLE_FRAME_EMPTY)

    def test_frame_from_raw(self) -> None:
        """Test parse FrameStatusRequestNotification from raw."""
        frame = frame_from_raw(self.EXAMPLE_FRAME_EMPTY)
        self.assertTrue(isinstance(frame, FrameStatusRequestNotification))

    def test_request_main_info_from_raw(self) -> None:
        """Test parse REQUEST_MAIN_INFO with 2-byte position fields."""
        frame = FrameStatusRequestNotification()
        frame.from_payload(bytes([
            0x47, 0x11,  # session_id
            0x02,  # status_id
            0x07,  # node_id
            RunStatus.EXECUTION_ACTIVE.value,
            StatusReply.COMMAND_COMPLETED_OK.value,
            StatusType.REQUEST_MAIN_INFO.value,
            0xC4, 0x00,  # target_position
            0xC3, 0xFF,  # current_position
            0x12, 0x34,  # remaining_time
            0x00, 0x65, 0x43, 0x21,  # last_master_execution_address
            0x02,  # last_command_originator
        ]))

        self.assertEqual(frame.session_id, 0x4711)
        self.assertEqual(frame.status_id, 0x02)
        self.assertEqual(frame.node_id, 0x07)
        self.assertEqual(frame.run_status, RunStatus.EXECUTION_ACTIVE)
        self.assertEqual(frame.status_reply, StatusReply.COMMAND_COMPLETED_OK)
        self.assertEqual(frame.status_type, StatusType.REQUEST_MAIN_INFO)
        self.assertEqual(frame.target_position, Parameter(bytes([0xC4, 0x00])))
        self.assertEqual(frame.current_position, Parameter(bytes([0xC3, 0xFF])))
        self.assertEqual(frame.remaining_time, 0x1234)
        self.assertEqual(frame.last_master_execution_address, bytes([0x00, 0x65, 0x43, 0x21]))
        self.assertEqual(frame.last_command_originator, 0x02)

    def test_request_main_info_roundtrip(self) -> None:
        """Test REQUEST_MAIN_INFO can be serialized and parsed again."""
        frame = FrameStatusRequestNotification()
        frame.session_id = 0x4711
        frame.status_id = 0x02
        frame.node_id = 0x07
        frame.run_status = RunStatus.EXECUTION_ACTIVE
        frame.status_reply = StatusReply.COMMAND_COMPLETED_OK
        frame.status_type = StatusType.REQUEST_MAIN_INFO
        frame.target_position = Parameter(bytes([0xC4, 0x00]))
        frame.current_position = Parameter(bytes([0xC3, 0xFF]))
        frame.remaining_time = 0x1234
        frame.last_master_execution_address = bytes([0x00, 0x65, 0x43, 0x21])
        frame.last_command_originator = 0x02

        restored = FrameStatusRequestNotification()
        restored.from_payload(frame.get_payload())

        self.assertEqual(restored.target_position, frame.target_position)
        self.assertEqual(restored.current_position, frame.current_position)
        self.assertEqual(restored.remaining_time, frame.remaining_time)
        self.assertEqual(restored.last_master_execution_address, frame.last_master_execution_address)
        self.assertEqual(restored.last_command_originator, frame.last_command_originator)

    def test_str(self) -> None:
        """Test string representation of FrameStatusRequestNotification."""
        frame = FrameStatusRequestNotification()
        self.assertEqual(str(frame), "<FrameStatusRequestNotification session_id=\"0\" "
                                     "status_id=\"0\" node_id=\"0\" run_status=\"RunStatus.EXECUTION_COMPLETED\" "
                                     "status_reply=\"StatusReply.UNKNOWN_STATUS_REPLY\" "
                                     "status_type=\"StatusType.REQUEST_TARGET_POSITION\" status_count=\"0\" "
                                     "parameter_data=\"\"/>")
