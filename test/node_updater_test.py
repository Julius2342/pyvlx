"""Unit test for NodeUpdater."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from pyvlx import Node, OpeningDevice, PyVLX
from pyvlx.api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification,
    FrameStatusRequestNotification,
)
from pyvlx.connection import Connection
from pyvlx.const import OperatingState, StatusReply
from pyvlx.node_updater import NodeUpdater


class TestNodeUpdater(IsolatedAsyncioTestCase):
    """Test class for NodeUpdater."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.pyvlx = MagicMock(spec=PyVLX)
        self.connection = MagicMock(spec=Connection)
        self.pyvlx.attach_mock(mock=self.connection, attribute="connection")
        self.node_updater = NodeUpdater(self.pyvlx)
        self.pyvlx.nodes = {}

    async def test_last_frame_state_set_on_node_state_position_changed(self) -> None:
        """Test that last_frame_state is set when FrameNodeStatePositionChangedNotification is received."""
        # Create a test node
        opening_device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=23, name="Test device"
        )
        self.pyvlx.nodes[23] = opening_device
        # Create a frame with state
        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 23
        frame.state = OperatingState.EXECUTING

        # Process the frame
        await self.node_updater.process_frame(frame)
        # Verify that last_frame_state was set
        self.assertEqual(opening_device.last_frame_state, OperatingState.EXECUTING)

    async def test_last_frame_state_set_on_all_nodes_information(self) -> None:
        """Test that last_frame_state is set when FrameGetAllNodesInformationNotification is received."""
        # Create a test node
        opening_device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=42, name="Test device 2"
        )
        self.pyvlx.nodes[42] = opening_device

        # Create a frame with state
        frame = FrameGetAllNodesInformationNotification()
        frame.node_id = 42
        frame.state = OperatingState.DONE

        # Process the frame
        await self.node_updater.process_frame(frame)

        # Verify that last_frame_state was set
        self.assertEqual(opening_device.last_frame_state, OperatingState.DONE)

    async def test_process_frame_status_request_notification(self) -> None:
        """Test process_frame_status_request_notification updates status."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 1
        mocked_node.last_frame_status_reply = None
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {1: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.BATTERY_LEVEL

        await updater.process_frame_status_request_notification(frame)

        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.BATTERY_LEVEL)
        mocked_node.after_update.assert_awaited_once()

    async def test_process_frame_status_request_notification_no_change(self) -> None:
        """Test process_frame_status_request_notification without changes."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 1
        mocked_node.last_frame_status_reply = StatusReply.BATTERY_LEVEL
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {1: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.BATTERY_LEVEL

        await updater.process_frame_status_request_notification(frame)

        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.BATTERY_LEVEL)
        mocked_node.after_update.assert_not_awaited()
