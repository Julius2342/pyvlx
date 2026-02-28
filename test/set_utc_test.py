"""Unit test for SetUTC module."""
import unittest
from unittest.mock import MagicMock, patch

from pyvlx.api import SetUTC
from pyvlx.api.frames import FrameSetUTCConfirmation, FrameSetUTCRequest


class TestSetUTC(unittest.IsolatedAsyncioTestCase):
    """Test class for SetUTC."""

    def setUp(self) -> None:
        """Set up TestSetUTC."""
        self.pyvlx = MagicMock()

    def test_explicit_timestamp(self) -> None:
        """Test that an explicit timestamp is stored correctly."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1234567890.0)
        self.assertEqual(set_utc.timestamp, 1234567890.0)

    def test_explicit_timestamp_float(self) -> None:
        """Test that a float timestamp is preserved."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1234567890.123)
        self.assertEqual(set_utc.timestamp, 1234567890.123)

    @patch("pyvlx.api.set_utc.time.time", return_value=1700000000.0)
    def test_default_timestamp_uses_current_time(self, mock_time: MagicMock) -> None:
        """Test that omitting timestamp uses time.time()."""
        set_utc = SetUTC(pyvlx=self.pyvlx)
        self.assertEqual(set_utc.timestamp, 1700000000.0)
        mock_time.assert_called_once()

    @patch("pyvlx.api.set_utc.time.time", return_value=1700000000.0)
    def test_default_timestamp_none_uses_current_time(self, mock_time: MagicMock) -> None:
        """Test that passing timestamp=None explicitly uses time.time()."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=None)
        self.assertEqual(set_utc.timestamp, 1700000000.0)
        mock_time.assert_called_once()

    @patch("pyvlx.api.set_utc.time.time")
    def test_multiple_calls_get_different_timestamps(self, mock_time: MagicMock) -> None:
        """Test that multiple SetUTC instances each capture their own timestamp."""
        mock_time.side_effect = [1700000000.0, 1700000005.0, 1700000010.0]

        set_utc_1 = SetUTC(pyvlx=self.pyvlx)
        set_utc_2 = SetUTC(pyvlx=self.pyvlx)
        set_utc_3 = SetUTC(pyvlx=self.pyvlx)

        self.assertEqual(set_utc_1.timestamp, 1700000000.0)
        self.assertEqual(set_utc_2.timestamp, 1700000005.0)
        self.assertEqual(set_utc_3.timestamp, 1700000010.0)
        self.assertEqual(mock_time.call_count, 3)

    @patch("pyvlx.api.set_utc.time.time")
    def test_multiple_calls_timestamp_captured_at_init(self, mock_time: MagicMock) -> None:
        """Test that timestamp is captured at __init__, not at request_frame time."""
        mock_time.return_value = 1700000000.0
        set_utc = SetUTC(pyvlx=self.pyvlx)

        # Advance mock time — should NOT affect the already-created instance
        mock_time.return_value = 1700099999.0

        frame = set_utc.request_frame()
        self.assertEqual(frame.timestamp, 1700000000)

    @patch("pyvlx.api.set_utc.time.time")
    def test_multiple_instances_independent_request_frames(self, mock_time: MagicMock) -> None:
        """Test that request_frame of each instance uses its own captured timestamp."""
        mock_time.side_effect = [1700000000.0, 1700000060.0]

        set_utc_1 = SetUTC(pyvlx=self.pyvlx)
        set_utc_2 = SetUTC(pyvlx=self.pyvlx)

        frame_1 = set_utc_1.request_frame()
        frame_2 = set_utc_2.request_frame()

        self.assertEqual(frame_1.timestamp, 1700000000)
        self.assertEqual(frame_2.timestamp, 1700000060)
        self.assertNotEqual(frame_1.timestamp, frame_2.timestamp)

    def test_initial_success_is_false(self) -> None:
        """Test that success is initially False."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1000.0)
        self.assertFalse(set_utc.success)

    async def test_handle_frame_confirmation(self) -> None:
        """Test handle_frame with a valid FrameSetUTCConfirmation."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1000.0)
        frame = FrameSetUTCConfirmation()
        result = await set_utc.handle_frame(frame)
        self.assertTrue(result)
        self.assertTrue(set_utc.success)

    async def test_handle_frame_wrong_frame_type(self) -> None:
        """Test handle_frame with an unrelated frame type returns False."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1000.0)
        frame = MagicMock()
        result = await set_utc.handle_frame(frame)
        self.assertFalse(result)
        self.assertFalse(set_utc.success)

    async def test_handle_frame_does_not_change_timestamp(self) -> None:
        """Test that handle_frame does not alter the stored timestamp."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1234567890.0)
        frame = FrameSetUTCConfirmation()
        await set_utc.handle_frame(frame)
        self.assertEqual(set_utc.timestamp, 1234567890.0)

    def test_request_frame_returns_correct_type(self) -> None:
        """Test that request_frame returns a FrameSetUTCRequest."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1700000000.5)
        frame = set_utc.request_frame()
        self.assertIsInstance(frame, FrameSetUTCRequest)

    def test_request_frame_truncates_to_int(self) -> None:
        """Test that request_frame truncates float timestamp to int."""
        set_utc = SetUTC(pyvlx=self.pyvlx, timestamp=1700000000.999)
        frame = set_utc.request_frame()
        self.assertEqual(frame.timestamp, 1700000000)

    @patch("pyvlx.api.set_utc.time.time")
    def test_multiple_calls_request_frame_called_twice_same_instance(self, mock_time: MagicMock) -> None:
        """Test that calling request_frame multiple times on the same instance returns the same timestamp."""
        mock_time.return_value = 1700000000.0
        set_utc = SetUTC(pyvlx=self.pyvlx)

        frame_1 = set_utc.request_frame()
        frame_2 = set_utc.request_frame()

        self.assertEqual(frame_1.timestamp, frame_2.timestamp)
        # time.time() should only have been called once — at __init__
        mock_time.assert_called_once()

    @patch("pyvlx.api.set_utc.time.time")
    def test_explicit_timestamp_does_not_call_time(self, mock_time: MagicMock) -> None:
        """Test that passing an explicit timestamp does not call time.time()."""
        SetUTC(pyvlx=self.pyvlx, timestamp=1234567890.0)
        mock_time.assert_not_called()
