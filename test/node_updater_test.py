"""Unit test for NodeUpdater."""
from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock

from pyvlx import OpeningDevice, Position, PyVLX
from pyvlx.api.frames import (
    FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification,
)
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
        self.assertEqual(opening_device.last_frame_state, OperatingState.EXECUTING)

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

    async def test_last_frame_state_updates_with_different_states(self) -> None:
        """Test that last_frame_state updates when multiple frames are received."""
        # Create a test node
        opening_device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=23, name="Test device"
        )
        self.pyvlx.nodes = MagicMock()
        self.pyvlx.nodes.__contains__ = MagicMock(return_value=True)
        self.pyvlx.nodes.__getitem__ = MagicMock(return_value=opening_device)

        # Verify initial state is None
        self.assertIsNone(opening_device.last_frame_state)

        # Process first frame with EXECUTING state
        frame1 = FrameNodeStatePositionChangedNotification()
        frame1.node_id = 23
        frame1.state = OperatingState.EXECUTING
        frame1.current_position = Position(position_percent=50)
        frame1.target = Position(position_percent=100)
        frame1.remaining_time = 10

        await self.node_updater.process_frame(frame1)
        self.assertEqual(opening_device.last_frame_state, OperatingState.EXECUTING)

        # Process second frame with DONE state
        frame2 = FrameNodeStatePositionChangedNotification()
        frame2.node_id = 23
        frame2.state = OperatingState.DONE
        frame2.current_position = Position(position_percent=100)
        frame2.target = Position(position_percent=100)
        frame2.remaining_time = 0

        await self.node_updater.process_frame(frame2)
        self.assertEqual(opening_device.last_frame_state, OperatingState.DONE)

    async def test_last_frame_state_type_is_operating_state(self) -> None:
        """Test that last_frame_state is of type OperatingState, not string."""
        # Create a test node
        opening_device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=23, name="Test device"
        )
        self.pyvlx.nodes = MagicMock()
        self.pyvlx.nodes.__contains__ = MagicMock(return_value=True)
        self.pyvlx.nodes.__getitem__ = MagicMock(return_value=opening_device)

        # Create a frame with state
        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 23
        frame.state = OperatingState.WAIT_FOR_POWER
        frame.current_position = Position(position_percent=0)
        frame.target = Position(position_percent=0)
        frame.remaining_time = 0

        # Process the frame
        await self.node_updater.process_frame(frame)

        # Verify that last_frame_state is OperatingState type, not string
        self.assertIsInstance(opening_device.last_frame_state, OperatingState)
        self.assertEqual(opening_device.last_frame_state, OperatingState.WAIT_FOR_POWER)
        # Ensure it's not converted to string
        self.assertNotIsInstance(opening_device.last_frame_state, str)
