"""Unit test for frame wink send."""
from unittest import TestCase

from pyvlx.api.frames.frame_wink_send import (
    FrameWinkSendConfirmation, FrameWinkSendNotification, FrameWinkSendRequest,
    WinkSendConfirmationStatus)
from pyvlx.const import Originator, Priority, WinkTime


class TestFrameWinkSendRequest(TestCase):
    """Test class for FrameWinkSendRequest."""

    def test_get_payload(self) -> None:
        """Test get_payload of FrameWinkSendRequest."""
        frame = FrameWinkSendRequest(
            node_ids=[1, 2],
            wink_time=WinkTime.BY_MANUFACTURER,
            session_id=258,
            originator=Originator.USER,
            priority=Priority.USER_LEVEL_2,
        )
        self.assertEqual(
            frame.get_payload(),
            b"\x01\x02"  # session id
            b"\x01"  # Originator user
            b"\x03"  # Priority user level 2
            b"\x01"  # WinkState enable
            b"\xfe"  # WinkTime 254
            b"\x02\x01\x02"  # 2 nodes: 1, 2
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # padding
        )

    def test_from_payload(self) -> None:
        """Test from_payload of FrameWinkSendRequest."""
        frame = FrameWinkSendRequest()
        frame.from_payload(
            b"\x01\x02"  # session id
            b"\x01"  # Originator user
            b"\x03"  # Priority user level 2
            b"\x01"  # WinkState enable
            b"\xfe"  # WinkTime 254
            b"\x02\x01\x02"  # 2 nodes: 1, 2
            b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # padding
        )
        self.assertEqual(frame.session_id, 258)
        self.assertEqual(frame.originator, Originator.USER)
        self.assertEqual(frame.priority, Priority.USER_LEVEL_2)
        self.assertEqual(frame.wink_time, WinkTime.BY_MANUFACTURER)
        self.assertEqual(frame.node_ids, [1, 2])

    def test_str(self) -> None:
        """Test __str__."""
        frame = FrameWinkSendRequest(
            node_ids=[1, 2],
            wink_time=WinkTime.BY_MANUFACTURER,
            session_id=258,
            originator=Originator.USER,
            priority=Priority.USER_LEVEL_2,
        )
        self.assertEqual(
            str(frame),
            '<FrameWinkSendRequest node_ids="[1, 2]" wink_time="WinkTime.BY_MANUFACTURER" session_id="258" originator="Originator.USER"/>',
        )


class TestFrameWinkSendConfirmation(TestCase):
    """Test class for FrameWinkSendConfirmation."""

    def test_get_payload(self) -> None:
        """Test get_payload."""
        frame = FrameWinkSendConfirmation(
            session_id=258, status=WinkSendConfirmationStatus.ACCEPTED
        )
        self.assertEqual(frame.get_payload(), b"\x01\x02\x01")

    def test_from_payload(self) -> None:
        """Test from_payload."""
        frame = FrameWinkSendConfirmation()
        frame.from_payload(b"\x01\x02\x01")
        self.assertEqual(frame.session_id, 258)
        self.assertEqual(frame.status, WinkSendConfirmationStatus.ACCEPTED)

    def test_str(self) -> None:
        """Test string."""
        frame = FrameWinkSendConfirmation(
            session_id=258, status=WinkSendConfirmationStatus.ACCEPTED
        )
        self.assertEqual(
            str(frame),
            '<FrameWinkSendConfirmation session_id="258" status="WinkSendConfirmationStatus.ACCEPTED"/>',
        )


class TestFrameWinkSendNotification(TestCase):
    """Test class for FrameWinkSendNotification."""

    def test_get_payload(self) -> None:
        """Test get_payload."""
        frame = FrameWinkSendNotification(session_id=258)
        self.assertEqual(frame.get_payload(), b"\x01\x02")

    def test_from_payload(self) -> None:
        """Test from_payload."""
        frame = FrameWinkSendNotification()
        frame.from_payload(b"\x01\x02")
        self.assertEqual(frame.session_id, 258)

    def test_str(self) -> None:
        """Test string."""
        frame = FrameWinkSendNotification(session_id=258)
        self.assertEqual(
            str(frame), '<FrameWinkSendNotification session_id="258"/>'
        )
