"""Unit tests for FrameSetUTCRequest."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameStatusRequestConfirmation, FrameStatusRequestRequest)
from pyvlx.api.frames.frame_status_request import (
    FrameStatusRequestNotification, StatusRequestStatus)


class TestFrameStatusRequestRequest(unittest.TestCase):
    """Test class FrameStatusRequestRequest."""

    # pylint: disable=too-many-public-methods,invalid-name

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

    # pylint: disable=too-many-public-methods,invalid-name

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

    # pylint: disable=too-many-public-methods,invalid-name

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
