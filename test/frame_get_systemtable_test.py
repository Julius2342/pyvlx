"""Unit tests for FrameGetSystemTable."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    FrameGetSystemTableConfirmation, FrameGetSystemTableNotification,
    FrameGetSystemTableRequest)
from pyvlx.const import Manufactor, NodeTypeWithSubtype, PowerMode, TurnAround


class TestFrameGetSystemTableRequest(unittest.TestCase):
    """Unit Test class for GetSystemTable."""

    def test_request_check_bytes(self):
        """Test FrameGetSystemTableRequest."""
        frame = FrameGetSystemTableRequest()
        self.assertEqual(bytes(frame), b"\x00\x03\x01\x00\x02")

    def test_request_frame_from_raw(self):
        """Test parse FrameGetSceneListConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x03\x01\x00\x02")
        self.assertTrue(isinstance(frame, FrameGetSystemTableRequest))

    def test_request_check_str(self):
        """Test string representation of FrameGetSceneListConfirmation."""
        frame = FrameGetSystemTableRequest()
        self.assertEqual(str(frame), '<FrameGetSystemTableRequest/>')

    def test_confirm_check_bytes(self):
        """Test FrameGetSystemTableConfirmation."""
        frame = FrameGetSystemTableConfirmation()
        self.assertEqual(bytes(frame), b"\x00\x03\x01\x01\x03")

    def test_confirm_frame_from_raw(self):
        """Test parse FrameGetSystemTableConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x03\x01\x01\x03")
        self.assertTrue(isinstance(frame, FrameGetSystemTableConfirmation))

    def test_confirm_check_str(self):
        """Test string representation of FrameGetSystemTableConfirmation."""
        frame = FrameGetSystemTableConfirmation()
        self.assertEqual(str(frame), '<FrameGetSystemTableConfirmation/>')

    EMPTY_NOTIFY = b"\x00\x05\x01\x02\x00\x72\x74"

    def test_notify_empty_bytes(self):
        """Test FrameGetSystemTableNotification."""
        frame = FrameGetSystemTableNotification()
        self.assertEqual(bytes(frame), b"\x00\x05\x01\x02\x00\x00\x06")

    def test_notify_empty_from_raw(self):
        """Test parse FrameGetSystemTableNotification from raw."""
        frame = frame_from_raw(self.EMPTY_NOTIFY)
        self.assertTrue(isinstance(frame, FrameGetSystemTableNotification))
        self.assertEqual(frame.remaining_objects, 114)
        self.assertEqual(len(frame.actutators), 0)

    def test_notify_empty_str(self):
        """Test parse FrameGetSystemTableNotification from raw."""
        frame = frame_from_raw(self.EMPTY_NOTIFY)
        self.assertEqual(str(frame), '<FrameGetSystemTableNotification objects="0" remaining_objects="114"></FrameGetSystemTableNotification>')

    ONE_NOTIFY = b"\x00\x10\x01\x02\x01\x01\x12\x34\x56\x05\x02\x72\x0B\x65\x43\x21\x71\x6B"

    def test_notify_one_from_raw(self):
        """Test FrameGetSystemTableNotification."""
        frame = frame_from_raw(self.ONE_NOTIFY)
        self.assertTrue(isinstance(frame, FrameGetSystemTableNotification))
        self.assertEqual(frame.remaining_objects, 113)
        self.assertEqual(len(frame.actutators), 1)
        self.assertEqual(frame.actutators[0].idx, 1)
        self.assertEqual(frame.actutators[0].address, b"\x12\x34\x56")
        self.assertEqual(frame.actutators[0].subtype, NodeTypeWithSubtype.VENTILATION_POINT_AIR_TRANSFER)
        self.assertEqual(frame.actutators[0].power_save_mode, PowerMode.LOW_POWER_MODE)
        self.assertEqual(frame.actutators[0].io, True)
        self.assertEqual(frame.actutators[0].rf, True)
        self.assertEqual(frame.actutators[0].turn_around_time, TurnAround.WITHIN_20MS)
        self.assertEqual(frame.actutators[0].manufactor, Manufactor.OVERKIZ)
        self.assertEqual(frame.actutators[0].backbone, b"\x65\x43\x21")

    def test_notify_one_str(self):
        """Test parse FrameGetSystemTableNotification from raw."""
        frame = frame_from_raw(self.ONE_NOTIFY)
        self.assertEqual(
            str(frame),
            '<FrameGetSystemTableNotification objects="1" remaining_objects="113">'
            '<Actutator index="1" address="18.52.86" type="VENTILATION_POINT" subtype="VENTILATION_POINT_AIR_TRANSFER" '
            'powerSaveMode="LOW_POWER_MODE" io="true" rf="true" turnAroundTime="WITHIN_20MS" manufactor="OVERKIZ" backbone="101.67.33"/>'
            '</FrameGetSystemTableNotification>'
        )
