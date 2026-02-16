"""Unit test for limitation."""
import asyncio
import unittest
from unittest.mock import MagicMock

import pytest
from pytest import FixtureRequest

from pyvlx import PyVLX
from pyvlx.api.frames.frame_set_limitation import (
    FrameSetLimitationConfirmation, FrameSetLimitationRequest,
    SetLimitationRequestStatus)
from pyvlx.api.set_limitation import SetLimitation
from pyvlx.const import Originator
from pyvlx.parameter import (
    IgnorePosition, LimitationTime, LimitationTimeClearAll, Position)


@pytest.fixture(scope="class")
def event_loop_instance(request: FixtureRequest) -> None:
    """Add the event_loop as an attribute to the unittest style test class."""
    request.cls.event_loop = asyncio.new_event_loop()
    yield
    request.cls.event_loop.close()


# pylint: disable=too-many-public-methods,invalid-name
@pytest.mark.usefixtures("event_loop_instance")
class TestSetLimitation(unittest.TestCase):
    """Test class for Limitation."""

    def setUp(self) -> None:
        """Set up TestSetLimitation."""
        self.pyvlx = MagicMock(spec=PyVLX)

    def test_handle_frames_accepted(self) -> None:
        """Test handle frame."""
        limit = SetLimitation(self.pyvlx, 1)

        frame = FrameSetLimitationConfirmation()
        frame.status = SetLimitationRequestStatus.ACCEPTED
        self.assertTrue(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertTrue(limit.success)

    def test_handle_frame_rejected(self) -> None:
        """Test handle frame."""
        limit = SetLimitation(self.pyvlx, 1)

        frame = FrameSetLimitationConfirmation()
        frame.status = SetLimitationRequestStatus.REJECTED
        self.assertTrue(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertFalse(limit.success)

    def test_request_frame(self) -> None:
        """Test initiating frame."""
        limit = SetLimitation(self.pyvlx, 1, Position(position_percent=30),
                              Position(position_percent=70), LimitationTime(seconds=60))
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameSetLimitationRequest)
        self.assertEqual(req_frame.node_ids, [1])
        self.assertEqual(req_frame.originator, Originator.USER)
        self.assertEqual(req_frame.limitation_value_min, Position(position_percent=30))
        self.assertEqual(req_frame.limitation_value_max, Position(position_percent=70))
        self.assertEqual(req_frame.limitation_time, LimitationTime(seconds=60))

    def test_request_clear_frame(self) -> None:
        """Test initiating frame."""
        limit = SetLimitation(self.pyvlx, 1, limitation_time=LimitationTimeClearAll())
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameSetLimitationRequest)
        self.assertEqual(req_frame.node_ids, [1])
        self.assertEqual(req_frame.originator, Originator.USER)
        self.assertEqual(req_frame.limitation_value_min, IgnorePosition())
        self.assertEqual(req_frame.limitation_value_max, IgnorePosition())
        self.assertEqual(req_frame.limitation_time, LimitationTimeClearAll())
