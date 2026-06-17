"""Unit test for limitation."""
import unittest
from unittest.mock import MagicMock

from pyvlx import PyVLX
from pyvlx.api.frames.frame_command_send import FrameSessionFinishedNotification
from pyvlx.api.frames.frame_get_limitation import FrameGetLimitationStatusNotification
from pyvlx.api.frames.frame_set_limitation import (
    FrameSetLimitationConfirmation, FrameSetLimitationRequest,
    SetLimitationRequestStatus)
from pyvlx.api.set_limitation import SetLimitation
from pyvlx.const import LimitationTime, Originator
from pyvlx.parameter import IgnorePosition, Position


class TestSetLimitation(unittest.IsolatedAsyncioTestCase):
    """Test class for Limitation."""

    def setUp(self) -> None:
        """Set up TestSetLimitation."""
        self.pyvlx = MagicMock(spec=PyVLX)

    async def test_handle_frames_accepted(self) -> None:
        """Test handle frame."""
        # command accepted does not mean it was successful, neither was the API call completed.
        limit = SetLimitation(self.pyvlx, 1)
        limit.session_id = 123

        frame = FrameSetLimitationConfirmation()
        frame.session_id = 123
        frame.status = SetLimitationRequestStatus.ACCEPTED
        self.assertFalse(await limit.handle_frame(frame))
        self.assertFalse(limit.success)

    async def test_handle_request_status_frame_rejected(self) -> None:
        """Test handle frame."""
        limit = SetLimitation(self.pyvlx, 1)
        limit.session_id = 123

        frame = FrameSetLimitationConfirmation()
        frame.session_id = 123
        frame.status = SetLimitationRequestStatus.REJECTED
        self.assertTrue(await limit.handle_frame(frame))
        self.assertFalse(limit.success)

    async def test_handle_request_status_frame_rejected_wrong_session_id(self) -> None:
        """Test handle frame."""
        # frames with wrong session id should be ignored, so the API call is not completed and success remains False.
        limit = SetLimitation(self.pyvlx, 1)
        limit.session_id = 123

        frame = FrameSetLimitationConfirmation()
        frame.session_id = 456
        frame.status = SetLimitationRequestStatus.REJECTED

        self.assertFalse(await limit.handle_frame(frame))
        self.assertFalse(limit.success)

    async def test_handle_limits_received_frame(self) -> None:
        """Test handle frame."""
        limit = SetLimitation(self.pyvlx, 1)
        limit.session_id = 123

        frame = FrameGetLimitationStatusNotification()
        frame.session_id = 123
        self.assertTrue(await limit.handle_frame(frame))
        self.assertTrue(limit.success)

    async def test_handle_limits_received_frame_wrong_session_id(self) -> None:
        """Test handle frame."""
        # frames with wrong session id should be ignored, so the API call is not completed and success remains False.
        limit = SetLimitation(self.pyvlx, 1)
        limit.session_id = 123

        frame = FrameGetLimitationStatusNotification()
        frame.session_id = 456
        self.assertFalse(await limit.handle_frame(frame))
        self.assertFalse(limit.success)

    async def test_handle_session_finished_frame(self) -> None:
        """Test handle frame."""
        limit = SetLimitation(self.pyvlx, 1)

        frame = FrameSessionFinishedNotification()
        self.assertTrue(await limit.handle_frame(frame))
        self.assertFalse(limit.success)

    async def test_handle_session_finished_frame_wrong_session_id(self) -> None:
        """Test handle frame."""
        # frames with wrong session id should be ignored, so the API call is not completed and success remains False.
        limit = SetLimitation(self.pyvlx, 1)
        limit.session_id = 123

        frame = FrameSessionFinishedNotification()
        frame.session_id = 456
        self.assertFalse(await limit.handle_frame(frame))
        self.assertFalse(limit.success)

    def test_request_frame(self) -> None:
        """Test initiating frame."""
        limit = SetLimitation(self.pyvlx, 1, Position(position_percent=30),
                              Position(position_percent=70))
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameSetLimitationRequest)
        self.assertEqual(req_frame.node_ids, [1])
        self.assertEqual(req_frame.originator, Originator.USER)
        self.assertEqual(req_frame.limitation_value_min, Position(position_percent=30))
        self.assertEqual(req_frame.limitation_value_max, Position(position_percent=70))
        self.assertEqual(req_frame.limitation_time, LimitationTime.UNLIMITED)

    def test_request_clear_frame(self) -> None:
        """Test initiating frame."""
        limit = SetLimitation(self.pyvlx, 1, limitation_time=LimitationTime.CLEAR_ALL)
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameSetLimitationRequest)
        self.assertEqual(req_frame.node_ids, [1])
        self.assertEqual(req_frame.originator, Originator.USER)
        self.assertEqual(req_frame.limitation_value_min, IgnorePosition())
        self.assertEqual(req_frame.limitation_value_max, IgnorePosition())
        self.assertEqual(req_frame.limitation_time, LimitationTime.CLEAR_ALL)

    def test_limitation_time_string(self) -> None:
        """Test string conversion of LimitationTime."""
        self.assertEqual(str(LimitationTime.UNLIMITED), "UNLIMITED")
