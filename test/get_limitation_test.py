"""Unit test for limitation."""
import asyncio
import unittest
from unittest.mock import MagicMock

import pytest
from pytest import FixtureRequest

from pyvlx import PyVLX
from pyvlx.api.frames.frame_get_limitation import (
    FrameGetLimitationStatus, FrameGetLimitationStatusConfirmation,
    FrameGetLimitationStatusNotification)
from pyvlx.api.get_limitation import GetLimitation
from pyvlx.const import LimitationType, Originator


@pytest.fixture(scope="class")
def event_loop_instance(request: FixtureRequest) -> None:
    """Add the event_loop as an attribute to the unittest style test class."""
    request.cls.event_loop = asyncio.new_event_loop()
    yield
    request.cls.event_loop.close()


# pylint: disable=too-many-public-methods,invalid-name
@pytest.mark.usefixtures("event_loop_instance")
class TestGetLimitation(unittest.TestCase):
    """Test class for Limitation."""

    def setUp(self) -> None:
        """Set up TestGetLimitation."""
        self.pyvlx = MagicMock(spec=PyVLX)

    def test_get_name(self) -> None:
        """Test get_name()."""
        limit = GetLimitation(self.pyvlx, 1)
        self.assertEqual(limit.node_id, 1)
        self.assertEqual(limit.limitation_type, LimitationType.MIN_LIMITATION)
        limit = GetLimitation(self.pyvlx, 2, LimitationType.MAX_LIMITATION)
        self.assertEqual(limit.node_id, 2)
        self.assertEqual(limit.limitation_type, LimitationType.MAX_LIMITATION)

    def test_max_value(self) -> None:
        """Test limit.max_value."""
        limit = GetLimitation(self.pyvlx, 1)
        limit.max_value_raw = b'\xf7'
        self.assertEqual(limit.max_value, 124)

    def test_min_value(self) -> None:
        """Test limit.min_value."""
        limit = GetLimitation(self.pyvlx, 1)
        limit.min_value_raw = b'\xba'
        self.assertEqual(limit.min_value, 93)

    def test_handle_frame(self) -> None:
        """Test handle frame."""
        limit = GetLimitation(self.pyvlx, 1)

        frame = FrameGetLimitationStatus()
        self.assertFalse(self.event_loop.run_until_complete(limit.handle_frame(frame)))
        self.assertFalse(limit.success)

        frame = FrameGetLimitationStatusConfirmation()
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
        self.assertEqual(limit.limit_time, frame.limit_time)

    def test_request_frame(self) -> None:
        """Test initiating frame."""
        limit = GetLimitation(self.pyvlx, 1)
        req_frame = limit.request_frame()
        self.assertIsInstance(req_frame, FrameGetLimitationStatus)
        self.assertTrue(req_frame.session_id, 1)
        self.assertTrue(req_frame.node_ids, [1])
        self.assertTrue(req_frame.limitations_type, limit.limitation_type)

        limit.limitation_type = LimitationType.MAX_LIMITATION
        self.assertIsInstance(req_frame, FrameGetLimitationStatus)
        self.assertTrue(req_frame.session_id, 1)
        self.assertTrue(req_frame.limitations_type, limit.limitation_type)
