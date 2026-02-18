"""Unit test for NodeUpdater."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from pyvlx import OpeningDevice, Position, PyVLX
from pyvlx.api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification)
from pyvlx.connection import Connection
from pyvlx.const import OperatingState
from pyvlx.node_updater import NodeUpdater


class TestNodeUpdater(IsolatedAsyncioTestCase):
    """Test class for NodeUpdater."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.pyvlx = MagicMock(spec=PyVLX)
        self.connection = MagicMock(spec=Connection)
        self.pyvlx.attach_mock(mock=self.connection, attribute="connection")
        self.node_updater = NodeUpdater(self.pyvlx)
        self.opening_device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=23, name="Test device"
        )
        self.pyvlx.nodes = {23: self.opening_device}

    async def test_last_frame_state_set_on_node_state_position_changed(self) -> None:
        """Test that last_frame_state is set when FrameNodeStatePositionChangedNotification is received."""
        # Create a frame with state
        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 23
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position_percent=50)
        frame.target = Position(position_percent=100)
        frame.remaining_time = 10

        # Process the frame
        await self.node_updater.process_frame(frame)
        # Verify that last_frame_state was set
        self.assertEqual(self.opening_device.last_frame_state, OperatingState.EXECUTING)

    async def test_last_frame_state_set_on_all_nodes_information(self) -> None:
        """Test that last_frame_state is set when FrameGetAllNodesInformationNotification is received."""
        # Create a test node
        opening_device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=42, name="Test device 2"
        )
        self.pyvlx.nodes = MagicMock()
        self.pyvlx.nodes.__contains__ = MagicMock(return_value=True)
        self.pyvlx.nodes.__getitem__ = MagicMock(return_value=opening_device)

        # Create a frame with state
        frame = FrameGetAllNodesInformationNotification()
        frame.node_id = 42
        frame.state = OperatingState.DONE
        frame.current_position = Position(position_percent=100)
        frame.target = Position(position_percent=100)
        frame.remaining_time = 0

        # Process the frame
        await self.node_updater.process_frame(frame)

        # Verify that last_frame_state was set
        self.assertEqual(opening_device.last_frame_state, OperatingState.DONE)
