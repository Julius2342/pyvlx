"""Unit tests for FrameActivateSceneConfirmation."""
import unittest

from pyvlx.api.frame_creation import frame_from_raw
from pyvlx.api.frames import (
    ActivateSceneConfirmationStatus, FrameActivateSceneConfirmation)


class TestFrameActivateSceneConfirmation(unittest.TestCase):
    """Test class FrameActivateSceneConfirmation."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_bytes(self):
        """Test FrameActivateSceneConfirmation."""
        frame = FrameActivateSceneConfirmation(
            session_id=1000, status=ActivateSceneConfirmationStatus.ACCEPTED
        )
        self.assertEqual(bytes(frame), b"\x00\x06\x04\x13\x00\x03\xe8\xfa")

    def test_bytes_error(self):
        """Test failed FrameActivateSceneConfirmation."""
        frame = FrameActivateSceneConfirmation(
            session_id=1000,
            status=ActivateSceneConfirmationStatus.ERROR_REQUEST_REJECTED,
        )
        self.assertEqual(bytes(frame), b"\x00\x06\x04\x13\x02\x03\xe8\xf8")

    def test_frame_from_raw(self):
        """Test parse FrameActivateSceneConfirmation from raw."""
        frame = frame_from_raw(b"\x00\x06\x04\x13\x02\x03\xe8\xf8")
        self.assertTrue(isinstance(frame, FrameActivateSceneConfirmation))
        self.assertEqual(
            frame.status, ActivateSceneConfirmationStatus.ERROR_REQUEST_REJECTED
        )
        self.assertEqual(frame.session_id, 1000)

    def test_str(self):
        """Test string representation of FrameActivateSceneConfirmation."""
        frame = FrameActivateSceneConfirmation(
            session_id=1000, status=ActivateSceneConfirmationStatus.ACCEPTED
        )
        self.assertEqual(
            str(frame),
            '<FrameActivateSceneConfirmation session_id="1000" status="ActivateSceneConfirmationStatus.ACCEPTED"/>',
        )
