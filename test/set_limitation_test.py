"""Unit test for limitation."""
import asyncio
import unittest

import pytest

from pyvlx import PyVLX
from pyvlx.api.frames.frame_set_limitation import (
    FrameSetLimitation, FrameSetLimitationConfirmation, SetLimitationRequestStatus)
from pyvlx.api.frames.frame_get_limitation import (
    FrameGetLimitationStatusNotification)
from pyvlx.api.set_limitation import SetLimitation
from pyvlx.const import Originator
from pyvlx.parameter import Position, IgnorePosition


@pytest.fixture(scope="class")
def event_loop_instance(request):
    """Add the event_loop as an attribute to the unittest style test class."""
    request.cls.event_loop = asyncio.get_event_loop_policy().new_event_loop()
    yield
    request.cls.event_loop.close()


# pylint: disable=too-many-public-methods,invalid-name
@pytest.mark.usefixtures("event_loop_instance")
class TestSetLimitation(unittest.TestCase):
    """Test class for Limitation."""

    def setUp(self):
        """Set up TestSetLimitation."""
        self.pyvlx = PyVLX()

    def test_handle_frames_accepted(self):
        """Test handle frame."""
        self.pyvlx = PyVLX()
        limit = SetLimitation(self.pyvlx, 1)

        frame = FrameSetLimitationConfirmation()
        frame.status = SetLimitationRequestStatus.ACCEPTED
        self.assertFalse(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertFalse(limit.success)

        frame = FrameGetLimitationStatusNotification()
        frame.session_id = 1
        frame.node_id = 1
        frame.min_value = b'\xf7'
        frame.max_value = b'\xba'
        frame.limit_originator = Originator.USER
        frame.limit_time = 1

        limit.session_id = 0
        self.assertFalse(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertFalse(limit.success)  # Session id is wrong

        limit.session_id = frame.session_id
        self.assertTrue(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertTrue(limit.success)

        self.assertEqual(limit.node_id, frame.node_id)
        self.assertEqual(limit.session_id, frame.session_id)
        self.assertEqual(limit.min_value, 124)
        self.assertEqual(limit.max_value, 93)
        self.assertEqual(limit.originator, frame.limit_originator)
        self.assertEqual(limit.limitation_time, frame.limit_time)

    def test_handle_frame_rejected(self):
        """Test handle frame."""
        self.pyvlx = PyVLX()
        limit = SetLimitation(self.pyvlx, 1)

        frame = FrameSetLimitationConfirmation()
        frame.status = SetLimitationRequestStatus.REJECTED
        self.assertTrue(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertFalse(limit.success)

    def test_request_frame(self):
        """Test initiating frame."""
        self.pyvlx = PyVLX()
        limit = SetLimitation(self.pyvlx, 1, Position(position_percent=30),
                              Position(position_percent=70))
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameSetLimitation)
        self.assertTrue(req_frame.session_id, 1)
        self.assertTrue(req_frame.node_ids, [1])
        self.assertTrue(req_frame.originator, Originator.USER)
        self.assertTrue(req_frame.limitation_value_min, Position(position_percent=30))
        self.assertTrue(req_frame.limitation_value_max, Position(position_percent=70))
        self.assertTrue(req_frame.limitation_time, 1)

    def test_request_clear_frame(self):
        """Test initiating frame."""
        self.pyvlx = PyVLX()
        limit = SetLimitation(self.pyvlx, 1, limitation_time=255)
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameSetLimitation)
        self.assertTrue(req_frame.session_id, 1)
        self.assertTrue(req_frame.node_ids, [1])
        self.assertTrue(req_frame.originator, Originator.USER)
        self.assertTrue(req_frame.limitation_value_min, IgnorePosition())
        self.assertTrue(req_frame.limitation_value_max, IgnorePosition())
        self.assertTrue(req_frame.limitation_time, 255)
 