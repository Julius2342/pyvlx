"""Unit test for NodeUpdater."""
# pylint: disable=too-many-public-methods
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from pyvlx import Node, OpeningDevice, PyVLX
from pyvlx.api.frames import (
    FrameCommandRunStatusNotification, FrameGetAllNodesInformationNotification,
    FrameNodeStatePositionChangedNotification, FrameStatusRequestNotification)
from pyvlx.connection import Connection
from pyvlx.const import NodeParameter, OperatingState, RunStatus, StatusReply
from pyvlx.dimmable_device import DimmableDevice
from pyvlx.node_updater import NodeUpdater
from pyvlx.on_off_switch import OnOffSwitch
from pyvlx.opening_device import Blind, DualRollerShutter
from pyvlx.parameter import Intensity, Parameter, Position, SwitchParameter


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
        mocked_node.last_frame_run_status = None
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
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {1: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.BATTERY_LEVEL
        frame.run_status = RunStatus.EXECUTION_COMPLETED

        await updater.process_frame_status_request_notification(frame)

        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.BATTERY_LEVEL)
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        mocked_node.after_update.assert_not_awaited()

    async def test_process_frame_status_request_notification_run_status_changed(self) -> None:
        """Test that run_status change triggers after_update and updates last_frame_run_status."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 1
        mocked_node.last_frame_status_reply = StatusReply.BATTERY_LEVEL
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_ACTIVE
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {1: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.BATTERY_LEVEL
        frame.run_status = RunStatus.EXECUTION_COMPLETED

        await updater.process_frame_status_request_notification(frame)

        # Verify run_status was updated
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.BATTERY_LEVEL)
        # Verify after_update was called
        mocked_node.after_update.assert_awaited_once()

    async def test_process_frame_status_request_notification_status_reply_changed(self) -> None:
        """Test that status_reply change triggers after_update and updates last_frame_status_reply."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 1
        mocked_node.last_frame_status_reply = StatusReply.BATTERY_LEVEL
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {1: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.run_status = RunStatus.EXECUTION_COMPLETED

        await updater.process_frame_status_request_notification(frame)

        # Verify status_reply was updated
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.UNKNOWN_STATUS_REPLY)
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        # Verify after_update was called
        mocked_node.after_update.assert_awaited_once()

    async def test_process_frame_status_request_notification_both_changed(self) -> None:
        """Test that both status_reply and run_status changes trigger after_update once."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 1
        mocked_node.last_frame_status_reply = StatusReply.BATTERY_LEVEL
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_ACTIVE
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {1: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.run_status = RunStatus.EXECUTION_COMPLETED

        await updater.process_frame_status_request_notification(frame)

        # Verify both were updated
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.UNKNOWN_STATUS_REPLY)
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        # Verify after_update was called only once despite both changing
        mocked_node.after_update.assert_awaited_once()

    async def test_blind_run_status_persisted_with_position_change(self) -> None:
        """Test that last_frame_run_status is persisted when Blind position also changes."""
        blind = Blind(
            pyvlx=self.pyvlx, node_id=1, name="Test blind", serial_number=None
        )
        blind.position = Position(position_percent=0)
        blind.orientation = Position(position_percent=0)
        blind.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        blind.last_frame_run_status = RunStatus.EXECUTION_ACTIVE
        blind.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[1] = blind

        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.parameter_data = {
            NodeParameter(0): Parameter(Position(position_percent=50).raw),
            NodeParameter(3): Parameter(Position(position_percent=75).raw),
        }

        await self.node_updater.process_frame_status_request_notification(frame)

        # Verify position changed
        self.assertEqual(blind.position, Position(position_percent=50))
        self.assertEqual(blind.orientation, Position(position_percent=75))
        # Verify run_status was persisted
        self.assertEqual(blind.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        # Verify after_update was called
        blind.after_update.assert_awaited_once()

    async def test_blind_position_changed_triggers_after_update(self) -> None:
        """Test that a Blind frame with changed position triggers after_update() once."""
        blind = Blind(
            pyvlx=self.pyvlx, node_id=1, name="Test blind", serial_number=None
        )
        blind.position = Position(position_percent=0)
        blind.orientation = Position(position_percent=0)
        blind.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        blind.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        blind.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[1] = blind

        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.parameter_data = {
            NodeParameter(0): Parameter(Position(position_percent=50).raw),
            NodeParameter(3): Parameter(Position(position_percent=75).raw),
        }

        await self.node_updater.process_frame_status_request_notification(frame)

        self.assertEqual(blind.position, Position(position_percent=50))
        self.assertEqual(blind.orientation, Position(position_percent=75))
        blind.after_update.assert_awaited_once()

    async def test_blind_no_change_skips_after_update(self) -> None:
        """Test that a Blind frame with unchanged position, status_reply and run_status does not trigger after_update()."""
        blind = Blind(
            pyvlx=self.pyvlx, node_id=1, name="Test blind", serial_number=None
        )
        blind.position = Position(position_percent=50)
        blind.orientation = Position(position_percent=75)
        blind.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        blind.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        blind.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[1] = blind

        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.parameter_data = {
            NodeParameter(0): Parameter(Position(position_percent=50).raw),
            NodeParameter(3): Parameter(Position(position_percent=75).raw),
        }

        await self.node_updater.process_frame_status_request_notification(frame)

        blind.after_update.assert_not_awaited()

    async def test_blind_missing_params_but_status_reply_changed(self) -> None:
        """Test that a Blind frame with missing MP/FP3 but changed status_reply triggers after_update()."""
        blind = Blind(
            pyvlx=self.pyvlx, node_id=1, name="Test blind", serial_number=None
        )
        blind.position = Position(position_percent=0)
        blind.orientation = Position(position_percent=0)
        blind.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        blind.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        blind.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[1] = blind

        frame = FrameStatusRequestNotification()
        frame.node_id = 1
        frame.status_reply = StatusReply.BATTERY_LEVEL
        frame.parameter_data = {}  # No MP or FP3

        await self.node_updater.process_frame_status_request_notification(frame)

        # Position should remain unchanged
        self.assertEqual(blind.position, Position(position_percent=0))
        self.assertEqual(blind.orientation, Position(position_percent=0))
        # But status_reply changed, so after_update should be called
        self.assertEqual(blind.last_frame_status_reply, StatusReply.BATTERY_LEVEL)
        blind.after_update.assert_awaited_once()

    async def test_dual_roller_shutter_position_changed_triggers_after_update(self) -> None:
        """Test that a DualRollerShutter frame with changed positions triggers after_update() once."""
        shutter = DualRollerShutter(
            pyvlx=self.pyvlx, node_id=2, name="Test shutter", serial_number=None
        )
        shutter.position = Position(position_percent=0)
        shutter.position_upper_curtain = Position(position_percent=0)
        shutter.position_lower_curtain = Position(position_percent=0)
        shutter.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        shutter.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        shutter.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[2] = shutter

        frame = FrameStatusRequestNotification()
        frame.node_id = 2
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.parameter_data = {
            NodeParameter(0): Parameter(Position(position_percent=30).raw),
            NodeParameter(1): Parameter(Position(position_percent=40).raw),
            NodeParameter(2): Parameter(Position(position_percent=60).raw),
        }

        await self.node_updater.process_frame_status_request_notification(frame)

        self.assertEqual(shutter.position, Position(position_percent=30))
        self.assertEqual(shutter.position_upper_curtain, Position(position_percent=40))
        self.assertEqual(shutter.position_lower_curtain, Position(position_percent=60))
        shutter.after_update.assert_awaited_once()

    async def test_dual_roller_shutter_no_change_skips_after_update(self) -> None:
        """Test that a DualRollerShutter frame with unchanged positions, status_reply and run_status does not trigger after_update()."""
        shutter = DualRollerShutter(
            pyvlx=self.pyvlx, node_id=2, name="Test shutter", serial_number=None
        )
        shutter.position = Position(position_percent=30)
        shutter.position_upper_curtain = Position(position_percent=40)
        shutter.position_lower_curtain = Position(position_percent=60)
        shutter.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        shutter.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        shutter.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[2] = shutter

        frame = FrameStatusRequestNotification()
        frame.node_id = 2
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.parameter_data = {
            NodeParameter(0): Parameter(Position(position_percent=30).raw),
            NodeParameter(1): Parameter(Position(position_percent=40).raw),
            NodeParameter(2): Parameter(Position(position_percent=60).raw),
        }

        await self.node_updater.process_frame_status_request_notification(frame)

        shutter.after_update.assert_not_awaited()

    async def test_dual_roller_shutter_missing_params_but_status_reply_changed(self) -> None:
        """Test that a DualRollerShutter frame with missing params but changed status_reply triggers after_update()."""
        shutter = DualRollerShutter(
            pyvlx=self.pyvlx, node_id=2, name="Test shutter", serial_number=None
        )
        shutter.position = Position(position_percent=0)
        shutter.position_upper_curtain = Position(position_percent=0)
        shutter.position_lower_curtain = Position(position_percent=0)
        shutter.last_frame_status_reply = StatusReply.UNKNOWN_STATUS_REPLY
        shutter.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        shutter.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[2] = shutter

        frame = FrameStatusRequestNotification()
        frame.node_id = 2
        frame.status_reply = StatusReply.BATTERY_LEVEL
        frame.parameter_data = {}  # No MP, FP1, or FP2

        await self.node_updater.process_frame_status_request_notification(frame)

        # Positions unchanged
        self.assertEqual(shutter.position, Position(position_percent=0))
        self.assertEqual(shutter.position_upper_curtain, Position(position_percent=0))
        self.assertEqual(shutter.position_lower_curtain, Position(position_percent=0))
        # But status_reply changed
        self.assertEqual(shutter.last_frame_status_reply, StatusReply.BATTERY_LEVEL)
        shutter.after_update.assert_awaited_once()

    # ── process_frame: after_update called when individual properties change ──

    async def test_after_update_called_when_position_changes(self) -> None:
        """Test that after_update() is called when position changes on an OpeningDevice."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=5, name="Test window"
        )
        device.position = Position(position_percent=0)
        device.last_frame_state = OperatingState.DONE
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[5] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 5
        frame.state = OperatingState.DONE
        frame.current_position = Position(position_percent=50)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertEqual(device.position, Position(position_percent=50))
        device.after_update.assert_awaited_once()

    async def test_after_update_called_when_is_opening_changes(self) -> None:
        """Test that after_update() is called when is_opening becomes True."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=6, name="Test window"
        )
        device.position = Position(position_percent=80)
        device.is_opening = False
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[6] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 6
        frame.state = OperatingState.EXECUTING
        # current_position > target → opening (higher raw value = more closed,
        # so position 80% current moving toward 20% target means opening)
        frame.current_position = Position(position_percent=80)
        frame.target = Position(position_percent=20)
        frame.remaining_time = 10

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_opening)
        device.after_update.assert_awaited_once()

    async def test_after_update_called_when_is_closing_changes(self) -> None:
        """Test that after_update() is called when is_closing becomes True."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=7, name="Test window"
        )
        device.position = Position(position_percent=20)
        device.is_closing = False
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[7] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 7
        frame.state = OperatingState.EXECUTING
        # current_position < target → closing
        frame.current_position = Position(position_percent=20)
        frame.target = Position(position_percent=80)
        frame.remaining_time = 10

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_closing)
        device.after_update.assert_awaited_once()

    async def test_is_opening_kept_via_cached_position_when_frame_current_position_is_ignore(self) -> None:
        """IGNORE current_position should fall back to the cached node position and keep is_opening set."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=70, name="Test gate"
        )
        device.position = Position(position_percent=100)
        device.target = Position(position_percent=0)
        device.is_opening = True
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[70] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 70
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.IGNORE)
        frame.target = Position(position_percent=0)
        frame.remaining_time = 3

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)
        device.after_update.assert_not_awaited()

    async def test_is_closing_kept_via_cached_position_when_frame_current_position_is_unknown(self) -> None:
        """UNKNOWN current_position should fall back to the cached node position and keep is_closing set."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=71, name="Test gate"
        )
        device.position = Position(position_percent=0)
        device.target = Position(position_percent=100)
        device.is_closing = True
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[71] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 71
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.UNKNOWN_VALUE)
        frame.target = Position(position_percent=100)
        frame.remaining_time = 3

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)
        device.after_update.assert_not_awaited()

    async def test_motion_state_preserved_when_cached_and_frame_positions_are_both_unavailable(self) -> None:
        """If neither the cached nor the frame position is concrete, an active opening state is preserved."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=74, name="Test gate"
        )
        device.position = Position(position=Parameter.UNKNOWN_VALUE)
        device.target = Position(position_percent=50)
        device.is_opening = True
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[74] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 74
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.UNKNOWN_VALUE)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 4

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)
        self.assertEqual(device.position, Position(position=Parameter.UNKNOWN_VALUE))
        self.assertIsNotNone(device.state_received_at)
        self.assertIsNotNone(device.estimated_completion)
        device.after_update.assert_not_awaited()

    async def test_closing_state_preserved_when_cached_and_frame_positions_are_both_unavailable(self) -> None:
        """If neither cached nor frame position is concrete, an active closing state is preserved too."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=76, name="Test gate"
        )
        device.position = Position(position=Parameter.UNKNOWN_VALUE)
        device.target = Position(position_percent=50)
        device.is_closing = True
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[76] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 76
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.UNKNOWN_VALUE)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 4

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)
        self.assertEqual(device.position, Position(position=Parameter.UNKNOWN_VALUE))
        self.assertIsNotNone(device.state_received_at)
        self.assertIsNotNone(device.estimated_completion)
        device.after_update.assert_not_awaited()

    async def test_motion_state_preserved_when_current_position_equals_target_while_executing(self) -> None:
        """Executing frames where current_position == target must not clear an active opening state."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=75, name="Test gate"
        )
        device.position = Position(position_percent=50)
        device.target = Position(position_percent=50)
        device.is_opening = True
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[75] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 75
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position_percent=50)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 2

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)
        self.assertEqual(device.position, Position(position_percent=50))
        self.assertIsNotNone(device.state_received_at)
        self.assertIsNotNone(device.estimated_completion)
        device.after_update.assert_not_awaited()

    async def test_closing_state_preserved_when_current_position_equals_target_while_executing(self) -> None:
        """Executing frames where current_position == target must not clear an active closing state either."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=77, name="Test gate"
        )
        device.position = Position(position_percent=50)
        device.target = Position(position_percent=50)
        device.is_closing = True
        device.last_frame_state = OperatingState.EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[77] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 77
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position_percent=50)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 2

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)
        self.assertEqual(device.position, Position(position_percent=50))
        self.assertIsNotNone(device.state_received_at)
        self.assertIsNotNone(device.estimated_completion)
        device.after_update.assert_not_awaited()

    async def test_motion_direction_derived_from_cached_position_when_frame_position_unknown(self) -> None:
        """Frames with IGNORE/UNKNOWN current_position should derive direction from the cached node position."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=72, name="Test gate"
        )
        device.position = Position(position_percent=100)
        device.target = Position(position_percent=0)
        device.is_opening = False
        device.is_closing = False
        device.last_frame_state = OperatingState.NON_EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[72] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 72
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.UNKNOWN_VALUE)
        frame.target = Position(position_percent=0)
        frame.remaining_time = 5

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)
        device.after_update.assert_awaited_once()

    async def test_closing_derived_from_new_target_when_frame_position_is_ignore(self) -> None:
        """A new higher target should indicate closing when the frame position is unavailable."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=78, name="Test gate"
        )
        device.position = Position(position_percent=100)
        device.target = Position(position_percent=0)
        device.is_opening = False
        device.is_closing = False
        device.last_frame_state = OperatingState.NOT_USED
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[78] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 78
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.IGNORE)
        frame.target = Position(position_percent=100)
        frame.remaining_time = 3

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)
        self.assertEqual(device.position, Position(position_percent=100))
        self.assertEqual(device.target, Position(position_percent=100))
        self.assertIsNotNone(device.state_received_at)
        self.assertIsNotNone(device.estimated_completion)
        device.after_update.assert_awaited_once()

    async def test_opening_derived_from_new_target_when_frame_position_is_unknown(self) -> None:
        """A new lower target should indicate opening when the frame position is unavailable."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=79, name="Test gate"
        )
        device.position = Position(position_percent=0)
        device.target = Position(position_percent=100)
        device.is_opening = False
        device.is_closing = False
        device.last_frame_state = OperatingState.NOT_USED
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[79] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 79
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.UNKNOWN_VALUE)
        frame.target = Position(position_percent=0)
        frame.remaining_time = 3

        await self.node_updater.process_frame(frame)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)
        self.assertEqual(device.position, Position(position_percent=0))
        self.assertEqual(device.target, Position(position_percent=0))
        self.assertIsNotNone(device.state_received_at)
        self.assertIsNotNone(device.estimated_completion)
        device.after_update.assert_awaited_once()

    async def test_idle_device_stays_idle_when_frame_position_unknown(self) -> None:
        """An idle device must not be marked as moving when the frame position is unavailable."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=73, name="Test gate"
        )
        device.position = Position(position=Parameter.UNKNOWN_VALUE)
        device.target = Position(position_percent=50)
        device.is_opening = False
        device.is_closing = False
        device.last_frame_state = OperatingState.NON_EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[73] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 73
        frame.state = OperatingState.EXECUTING
        frame.current_position = Position(position=Parameter.UNKNOWN_VALUE)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 5

        await self.node_updater.process_frame(frame)

        self.assertFalse(device.is_opening)
        self.assertFalse(device.is_closing)

    async def test_gate_opening_live_sequence_keeps_direction_until_done(self) -> None:
        """Live gate sequence should keep opening through IGNORE frames and stop on DONE."""
        device = OpeningDevice(pyvlx=self.pyvlx, node_id=80, name="Test gate")
        device.position = Position(position_percent=100)
        device.target = Position(position_percent=100)
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[80] = device

        start_frame = FrameNodeStatePositionChangedNotification()
        start_frame.node_id = 80
        start_frame.state = OperatingState.EXECUTING
        start_frame.current_position = Position(position_percent=100)
        start_frame.target = Position(position_percent=0)
        start_frame.remaining_time = 1

        await self.node_updater.process_frame(start_frame)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)
        self.assertEqual(device.position, Position(position_percent=100))
        self.assertEqual(device.target, Position(position_percent=0))

        for _ in range(2):
            ignore_frame = FrameNodeStatePositionChangedNotification()
            ignore_frame.node_id = 80
            ignore_frame.state = OperatingState.EXECUTING
            ignore_frame.current_position = Position(position=Parameter.IGNORE)
            ignore_frame.target = Position(position_percent=0)
            ignore_frame.remaining_time = 3

            await self.node_updater.process_frame(ignore_frame)

            self.assertTrue(device.is_opening)
            self.assertFalse(device.is_closing)
            self.assertEqual(device.position, Position(position_percent=100))
            self.assertEqual(device.target, Position(position_percent=0))

        command_status = FrameCommandRunStatusNotification(
            session_id=2,
            status_id=1,
            index_id=80,
            node_parameter=0,
            parameter_value=Parameter.UNKNOWN_VALUE,
            run_status=RunStatus.EXECUTION_COMPLETED,
            status_reply=StatusReply.COMMAND_OVERRULED,
        )

        await self.node_updater.process_frame(command_status)

        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)

        done_frame = FrameNodeStatePositionChangedNotification()
        done_frame.node_id = 80
        done_frame.state = OperatingState.DONE
        done_frame.current_position = Position(position_percent=0)
        done_frame.target = Position(position_percent=0)
        done_frame.remaining_time = 0

        await self.node_updater.process_frame(done_frame)

        self.assertFalse(device.is_opening)
        self.assertFalse(device.is_closing)
        self.assertEqual(device.position, Position(position_percent=0))
        self.assertEqual(device.target, Position(position_percent=0))

    async def test_gate_closing_live_sequence_keeps_direction_until_done(self) -> None:
        """Live gate sequence should keep closing through IGNORE frames and stop on DONE."""
        device = OpeningDevice(pyvlx=self.pyvlx, node_id=81, name="Test gate")
        device.position = Position(position_percent=0)
        device.target = Position(position_percent=0)
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[81] = device

        start_frame = FrameNodeStatePositionChangedNotification()
        start_frame.node_id = 81
        start_frame.state = OperatingState.EXECUTING
        start_frame.current_position = Position(position_percent=0)
        start_frame.target = Position(position_percent=100)
        start_frame.remaining_time = 1

        await self.node_updater.process_frame(start_frame)

        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)
        self.assertEqual(device.position, Position(position_percent=0))
        self.assertEqual(device.target, Position(position_percent=100))

        for _ in range(2):
            ignore_frame = FrameNodeStatePositionChangedNotification()
            ignore_frame.node_id = 81
            ignore_frame.state = OperatingState.EXECUTING
            ignore_frame.current_position = Position(position=Parameter.IGNORE)
            ignore_frame.target = Position(position_percent=100)
            ignore_frame.remaining_time = 3

            await self.node_updater.process_frame(ignore_frame)

            self.assertTrue(device.is_closing)
            self.assertFalse(device.is_opening)
            self.assertEqual(device.position, Position(position_percent=0))
            self.assertEqual(device.target, Position(position_percent=100))

        command_status = FrameCommandRunStatusNotification(
            session_id=2,
            status_id=1,
            index_id=81,
            node_parameter=0,
            parameter_value=Parameter.UNKNOWN_VALUE,
            run_status=RunStatus.EXECUTION_COMPLETED,
            status_reply=StatusReply.COMMAND_OVERRULED,
        )

        await self.node_updater.process_frame(command_status)

        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)

        done_frame = FrameNodeStatePositionChangedNotification()
        done_frame.node_id = 81
        done_frame.state = OperatingState.DONE
        done_frame.current_position = Position(position_percent=100)
        done_frame.target = Position(position_percent=100)
        done_frame.remaining_time = 0

        await self.node_updater.process_frame(done_frame)

        self.assertFalse(device.is_closing)
        self.assertFalse(device.is_opening)
        self.assertEqual(device.position, Position(position_percent=100))
        self.assertEqual(device.target, Position(position_percent=100))

    async def test_after_update_called_when_last_frame_state_changes(self) -> None:
        """Test that after_update() is called when last_frame_state changes."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=8, name="Test window"
        )
        device.last_frame_state = OperatingState.NON_EXECUTING
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[8] = device

        frame = FrameGetAllNodesInformationNotification()
        frame.node_id = 8
        frame.state = OperatingState.DONE
        frame.current_position = Position(position_percent=50)
        frame.target = Position(position_percent=50)
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertEqual(device.last_frame_state, OperatingState.DONE)
        device.after_update.assert_awaited_once()

    async def test_after_update_called_when_parameter_changes_from_off_to_on_switch(self) -> None:
        """Test that after_update() is called when parameter changes from OFF to ON on an OnOffSwitch."""
        switch = OnOffSwitch(
            pyvlx=self.pyvlx, node_id=9, name="Test switch", serial_number=None
        )
        switch.parameter = SwitchParameter(state=Parameter.OFF)
        switch.after_update = AsyncMock()  # type: ignore[method-assign]
        switch.last_frame_state = OperatingState.DONE
        self.pyvlx.nodes[9] = switch

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 9
        frame.state = OperatingState.DONE
        # Both current and target set to ON so the branch enters
        frame.current_position = Parameter(Parameter.from_int(Parameter.ON))
        frame.target = Parameter(Parameter.from_int(Parameter.ON))
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertTrue(switch.parameter.is_on())
        switch.after_update.assert_awaited_once()

    async def test_after_update_called_when_parameter_changes_from_on_to_off_switch(self) -> None:
        """Test that after_update() is called when parameter changes from ON to OFF on an OnOffSwitch."""
        switch = OnOffSwitch(
            pyvlx=self.pyvlx, node_id=9, name="Test switch", serial_number=None
        )
        switch.parameter = SwitchParameter(state=Parameter.ON)
        switch.last_frame_state = OperatingState.DONE
        switch.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[9] = switch

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 9
        frame.state = OperatingState.DONE
        # Both current and target set to OFF so the branch enters
        frame.current_position = Parameter(Parameter.from_int(Parameter.OFF))
        frame.target = Parameter(Parameter.from_int(Parameter.OFF))
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertTrue(switch.parameter.is_off())
        switch.after_update.assert_awaited_once()

    async def test_after_update_called_when_intensity_changes_dimmable(self) -> None:
        """Test that after_update() is called when intensity changes on a DimmableDevice."""
        device = DimmableDevice(
            pyvlx=self.pyvlx, node_id=10, name="Test light", serial_number=None
        )
        device.intensity = Intensity(intensity_percent=0)
        device.last_frame_state = OperatingState.DONE
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[10] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 10
        frame.state = OperatingState.DONE
        frame.current_position = Intensity(intensity_percent=75)
        frame.target = Intensity(intensity_percent=75)
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertEqual(device.intensity, Intensity(intensity_percent=75))
        device.after_update.assert_awaited_once()

    async def test_after_update_called_when_is_opening_stops(self) -> None:
        """Test that after_update() is called when is_opening transitions from True to False."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=11, name="Test window"
        )
        device.position = Position(position_percent=20)
        device.last_frame_state = OperatingState.DONE
        device.is_opening = True
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[11] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 11
        frame.state = OperatingState.DONE
        # position == target, not executing → stops opening
        frame.current_position = Position(position_percent=20)
        frame.target = Position(position_percent=20)
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertFalse(device.is_opening)
        device.after_update.assert_awaited_once()

    async def test_after_update_called_when_is_closing_stops(self) -> None:
        """Test that after_update() is called when is_closing transitions from True to False."""
        device = OpeningDevice(
            pyvlx=self.pyvlx, node_id=12, name="Test window"
        )
        device.position = Position(position_percent=80)
        device.last_frame_state = OperatingState.DONE
        device.is_closing = True
        device.after_update = AsyncMock()  # type: ignore[method-assign]
        self.pyvlx.nodes[12] = device

        frame = FrameNodeStatePositionChangedNotification()
        frame.node_id = 12
        frame.state = OperatingState.DONE
        # position == target, not executing → stops closing
        frame.current_position = Position(position_percent=80)
        frame.target = Position(position_percent=80)
        frame.remaining_time = 0

        await self.node_updater.process_frame(frame)

        self.assertFalse(device.is_closing)
        device.after_update.assert_awaited_once()

    async def test_process_command_run_status_notification(self) -> None:
        """Test process_frame with FrameCommandRunStatusNotification updates node and calls after_update."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 5
        mocked_node.last_frame_run_status = None
        mocked_node.last_frame_status_reply = None
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {5: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameCommandRunStatusNotification()
        frame.index_id = 5
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.status_reply = StatusReply.COMMAND_COMPLETED_OK

        await updater.process_frame(frame)

        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.COMMAND_COMPLETED_OK)
        mocked_node.after_update.assert_awaited_once()

    async def test_process_command_run_status_notification_run_status_changed(self) -> None:
        """Test that FrameCommandRunStatusNotification with only run_status change triggers after_update."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 5
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_ACTIVE
        mocked_node.last_frame_status_reply = StatusReply.COMMAND_COMPLETED_OK
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {5: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameCommandRunStatusNotification()
        frame.index_id = 5
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.status_reply = StatusReply.COMMAND_COMPLETED_OK

        await updater.process_frame(frame)

        # Verify run_status was updated
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.COMMAND_COMPLETED_OK)
        # Verify after_update was called
        mocked_node.after_update.assert_awaited_once()

    async def test_process_command_run_status_notification_status_reply_changed(self) -> None:
        """Test that FrameCommandRunStatusNotification with only status_reply change triggers after_update."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 5
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        mocked_node.last_frame_status_reply = StatusReply.COMMAND_COMPLETED_OK
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {5: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameCommandRunStatusNotification()
        frame.index_id = 5
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.status_reply = StatusReply.UNKNOWN_STATUS_REPLY

        await updater.process_frame(frame)

        # Verify status_reply was updated
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.UNKNOWN_STATUS_REPLY)
        # Verify after_update was called
        mocked_node.after_update.assert_awaited_once()

    async def test_process_command_run_status_notification_none_index_id(self) -> None:
        """Test process_frame with FrameCommandRunStatusNotification with None index_id returns early."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 5
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {5: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameCommandRunStatusNotification()
        frame.index_id = None
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.status_reply = StatusReply.COMMAND_COMPLETED_OK

        await updater.process_frame(frame)

        # after_update should NOT be called
        mocked_node.after_update.assert_not_awaited()

    async def test_process_command_run_status_notification_unknown_node_id(self) -> None:
        """Test process_frame with FrameCommandRunStatusNotification with unknown node_id returns early."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 5
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {5: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameCommandRunStatusNotification()
        frame.index_id = 99  # unknown node
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.status_reply = StatusReply.COMMAND_COMPLETED_OK

        await updater.process_frame(frame)

        # after_update should NOT be called
        mocked_node.after_update.assert_not_awaited()

    async def test_process_command_run_status_notification_no_change(self) -> None:
        """Test that FrameCommandRunStatusNotification with unchanged run_status and status_reply skips after_update()."""
        mocked_pyvlx = MagicMock(spec=PyVLX)
        mocked_node = MagicMock(spec=Node)
        mocked_node.name = "Test node"
        mocked_node.node_id = 5
        mocked_node.last_frame_run_status = RunStatus.EXECUTION_COMPLETED
        mocked_node.last_frame_status_reply = StatusReply.COMMAND_COMPLETED_OK
        mocked_node.after_update = AsyncMock()
        mocked_pyvlx.nodes = {5: mocked_node}

        updater = NodeUpdater(pyvlx=mocked_pyvlx)
        frame = FrameCommandRunStatusNotification()
        frame.index_id = 5
        frame.run_status = RunStatus.EXECUTION_COMPLETED
        frame.status_reply = StatusReply.COMMAND_COMPLETED_OK

        await updater.process_frame(frame)

        # Verify values remain unchanged
        self.assertEqual(mocked_node.last_frame_run_status, RunStatus.EXECUTION_COMPLETED)
        self.assertEqual(mocked_node.last_frame_status_reply, StatusReply.COMMAND_COMPLETED_OK)
        # Verify after_update was NOT called when nothing changed
        mocked_node.after_update.assert_not_awaited()
