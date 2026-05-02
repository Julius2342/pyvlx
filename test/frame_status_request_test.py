"""Unit tests for FrameSetUTCRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameStatusRequestConfirmation, FrameStatusRequestRequest)
from pyvlx.api.frames.frame_status_request import (
    FrameStatusRequestNotification, StatusRequestStatus)


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

    def test_from_raw_with_non_consecutive_node_ids(self) -> None:
        """Test parse FrameStatusRequestRequest preserves encoded node IDs."""
        raw = b"\x00\x1d\x03\x05\x00\xab\x02\x2a\x57" + bytes(18) + b"\x01\xfe\x000"

        frame = frame_from_raw(raw)

        self.assertTrue(isinstance(frame, FrameStatusRequestRequest))
        assert isinstance(frame, FrameStatusRequestRequest)
        self.assertEqual(frame.node_ids, [42, 87])

    def test_request_with_non_consecutive_node_ids_roundtrip(self) -> None:
        """Test FrameStatusRequestRequest survives a payload roundtrip with non-consecutive IDs."""
        frame = FrameStatusRequestRequest(node_ids=[42, 87, 7], session_id=0x00ab)
        restored = FrameStatusRequestRequest()

        restored.from_payload(frame.get_payload())

        self.assertEqual(restored.session_id, frame.session_id)
        self.assertEqual(restored.node_ids, frame.node_ids)
        self.assertEqual(restored.status_type, frame.status_type)
        self.assertEqual(restored.fpi1, frame.fpi1)
        self.assertEqual(restored.fpi2, frame.fpi2)

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

    def test_str(self) -> None:
        """Test string representation of FrameStatusRequestNotification."""
        frame = FrameStatusRequestNotification()
        self.assertEqual(str(frame), "<FrameStatusRequestNotification session_id=\"0\" "
                                     "status_id=\"0\" node_id=\"0\" run_status=\"RunStatus.EXECUTION_COMPLETED\" "
                                     "status_reply=\"StatusReply.UNKNOWN_STATUS_REPLY\" "
                                     "status_type=\"StatusType.REQUEST_TARGET_POSITION\" status_count=\"0\" "
                                     "parameter_data=\"\"/>")
