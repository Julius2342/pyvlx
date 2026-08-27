"""Unit tests for heartbeat module."""
import asyncio
from collections.abc import Coroutine
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import PyVLX
from pyvlx.exception import PyVLXException
from pyvlx.heartbeat import Heartbeat
from pyvlx.opening_device import Blind, Gate


class TestHeartbeat(IsolatedAsyncioTestCase):
    """Test class for Heartbeat."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.pyvlx = MagicMock(spec=PyVLX)
        self.pyvlx.connection = MagicMock()
        self.pyvlx.nodes = []

    def test_stopped_property(self) -> None:
        """Test stopped property reflects task state."""
        heartbeat = Heartbeat(self.pyvlx)

        self.assertTrue(heartbeat.stopped)
        running_task = MagicMock(spec=asyncio.Task)
        running_task.done.return_value = False
        heartbeat.heartbeat_task = running_task
        self.assertFalse(heartbeat.stopped)

    def test_stopped_property_when_task_died(self) -> None:
        """Test stopped returns True when task finished unexpectedly."""
        heartbeat = Heartbeat(self.pyvlx)
        dead_task = MagicMock(spec=asyncio.Task)
        dead_task.done.return_value = True
        heartbeat.heartbeat_task = dead_task
        self.assertTrue(heartbeat.stopped)

    async def test_start_is_idempotent(self) -> None:
        """Test start() does nothing if heartbeat is already running."""
        heartbeat = Heartbeat(self.pyvlx)
        existing_task = MagicMock(spec=asyncio.Task)
        existing_task.done.return_value = False
        heartbeat.heartbeat_task = existing_task

        with patch("pyvlx.heartbeat.asyncio.create_task") as create_task:
            await heartbeat.start()

        create_task.assert_not_called()
        self.assertEqual(heartbeat.heartbeat_task, existing_task)

    async def test_start_restarts_dead_task(self) -> None:
        """Test start() creates a new task when the existing one has died."""
        heartbeat = Heartbeat(self.pyvlx)
        dead_task = MagicMock(spec=asyncio.Task)
        dead_task.done.return_value = True
        dead_task.cancelled.return_value = False
        dead_task.exception.return_value = RuntimeError("boom")
        heartbeat.heartbeat_task = dead_task
        new_task = MagicMock(spec=asyncio.Task)

        def create_task_side_effect(coro: Coroutine) -> MagicMock:
            coro.close()
            return new_task

        with patch("pyvlx.heartbeat.asyncio.create_task", side_effect=create_task_side_effect) as mock_create_task:
            await heartbeat.start()

        dead_task.exception.assert_called_once()
        mock_create_task.assert_called_once()
        self.assertEqual(heartbeat.heartbeat_task, new_task)

    async def test_start_serializes_concurrent_calls(self) -> None:
        """Test concurrent start() calls only create one heartbeat task."""
        heartbeat = Heartbeat(self.pyvlx)
        created_task = MagicMock(spec=asyncio.Task)
        created_task.done.return_value = False

        def create_task_side_effect(coro: Coroutine) -> MagicMock:
            coro.close()
            return created_task

        with patch("pyvlx.heartbeat.asyncio.create_task", side_effect=create_task_side_effect) as mock_create_task:
            await asyncio.gather(heartbeat.start(), heartbeat.start())

        mock_create_task.assert_called_once()
        self.assertEqual(heartbeat.heartbeat_task, created_task)

    async def test_stop_without_running_task(self) -> None:
        """Test stop() returns cleanly when no task is active."""
        heartbeat = Heartbeat(self.pyvlx)

        await heartbeat.stop()

        self.assertIsNone(heartbeat.heartbeat_task)

    async def test_stop_cancels_running_task(self) -> None:
        """Test stop() cancels and awaits an active task."""
        heartbeat = Heartbeat(self.pyvlx)
        running_task = asyncio.create_task(asyncio.sleep(10))
        heartbeat.heartbeat_task = running_task

        await heartbeat.stop()

        self.assertTrue(running_task.cancelled())
        self.assertIsNone(heartbeat.heartbeat_task)

    @patch("pyvlx.heartbeat.GetState")
    async def test_pulse_raises_if_get_state_fails(self, get_state_cls: MagicMock) -> None:
        """Test pulse() raises exception if get state call fails."""
        get_state = MagicMock()
        get_state.do_api_call = AsyncMock()
        get_state.success = False
        get_state_cls.return_value = get_state
        heartbeat = Heartbeat(self.pyvlx)

        with self.assertRaises(PyVLXException):
            await heartbeat.pulse()

    @patch("pyvlx.heartbeat.asyncio.sleep", new_callable=AsyncMock)
    @patch("pyvlx.heartbeat.GetState")
    async def test_pulse_loads_only_blind_nodes_when_configured(
        self,
        get_state_cls: MagicMock,
        sleep_mock: AsyncMock,
    ) -> None:
        """Test pulse() requests status only for blind-type nodes when load_all_states is disabled."""
        blind = MagicMock(spec=Blind)
        blind.is_opening = False
        blind.is_closing = False
        non_blind = MagicMock()
        non_blind.node_id = 2
        self.pyvlx.nodes = [blind, non_blind]

        get_state = MagicMock()
        get_state.do_api_call = AsyncMock()
        get_state.success = True
        get_state_cls.return_value = get_state

        heartbeat = Heartbeat(self.pyvlx, load_all_states=False)
        await heartbeat.pulse()

        blind.update_status.assert_awaited_once()
        non_blind.update_status.assert_not_called()
        sleep_mock.assert_awaited_once_with(0.5)

    @patch("pyvlx.heartbeat.asyncio.sleep", new_callable=AsyncMock)
    @patch("pyvlx.heartbeat.GetState")
    async def test_pulse_loads_all_nodes_when_enabled(
        self,
        get_state_cls: MagicMock,
        sleep_mock: AsyncMock,
    ) -> None:
        """Test pulse() requests status for every node when load_all_states is enabled."""
        node_1 = AsyncMock()
        node_1.is_closing = False
        node_1.is_opening = False
        node_2 = AsyncMock()
        node_2.is_closing = False
        node_2.is_opening = False
        self.pyvlx.nodes = [node_1, node_2]

        get_state = MagicMock()
        get_state.do_api_call = AsyncMock()
        get_state.success = True
        get_state_cls.return_value = get_state

        heartbeat = Heartbeat(self.pyvlx, load_all_states=True)
        await heartbeat.pulse()

        assert node_1.update_status.await_count == 1
        assert node_2.update_status.await_count == 1
        self.assertEqual(sleep_mock.await_count, 2)

    @patch("pyvlx.heartbeat.asyncio.sleep", new_callable=AsyncMock)
    @patch("pyvlx.heartbeat.GetState")
    async def test_pulse_skips_opening_devices_in_motion(
        self,
        get_state_cls: MagicMock,
        sleep_mock: AsyncMock,
    ) -> None:
        """Skip status polling for any OpeningDevice currently in motion.

        Polling a node mid-travel can cause the KLF200 to report the
        active command as completed prematurely and, on some actuators,
        interrupt the motion. The heartbeat must therefore skip any
        OpeningDevice with is_opening or is_closing set.
        """
        moving_gate = MagicMock(spec=Gate)
        moving_gate.is_closing = True
        moving_gate.is_opening = False
        moving_gate.name = "Moving Gate"
        idle_node = AsyncMock()
        self.pyvlx.nodes = [moving_gate, idle_node]

        get_state = MagicMock()
        get_state.do_api_call = AsyncMock()
        get_state.success = True
        get_state_cls.return_value = get_state

        heartbeat = Heartbeat(self.pyvlx, load_all_states=True)
        await heartbeat.pulse()

        # Only the idle node was polled; the moving gate was skipped.
        idle_node.update_status.assert_awaited_once()
        moving_gate.update_status.assert_not_called()

        sleep_mock.assert_awaited_once_with(0.5)
