"""Unit test for Nodes object."""
import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import Blind, Nodes, PyVLX, RollerShutter, Window
from pyvlx.connection import Connection
from pyvlx.const import OperatingState, StatusReply
from pyvlx.node import Node


class TestNodes(unittest.TestCase):
    """Test class for nodes object."""

    def setUp(self) -> None:
        """Set up TestNodes."""
        self.pyvlx = MagicMock(spec=PyVLX)
        connection = MagicMock(spec=Connection)
        self.pyvlx.attach_mock(mock=connection, attribute="connection")

    def test_get_item(self) -> None:
        """Test get_item."""
        nodes = Nodes(self.pyvlx)
        window = Window(self.pyvlx, 0, "Window", "aa:bb:aa:bb:aa:bb:aa:00")
        nodes.add(window)
        blind = Blind(self.pyvlx, 1, "Blind", "aa:bb:aa:bb:aa:bb:aa:01")
        nodes.add(blind)
        roller_shutter = RollerShutter(
            self.pyvlx, 4, "Roller Shutter", "aa:bb:aa:bb:aa:bb:aa:04"
        )
        nodes.add(roller_shutter)
        self.assertEqual(nodes["Window"], window)
        self.assertEqual(nodes["Blind"], blind)
        self.assertEqual(nodes["Roller Shutter"], roller_shutter)
        self.assertEqual(nodes[0], window)
        self.assertEqual(nodes[1], blind)
        self.assertEqual(nodes[4], roller_shutter)

    def test_get_item_failed(self) -> None:
        """Test get_item with non existing object."""
        nodes = Nodes(self.pyvlx)
        window1 = Window(self.pyvlx, 0, "Window_1", "aa:bb:aa:bb:aa:bb:aa:00")
        nodes.add(window1)
        with self.assertRaises(KeyError):
            nodes["Window_2"]  # pylint: disable=pointless-statement
        with self.assertRaises(KeyError):
            nodes[1]  # pylint: disable=pointless-statement

    def test_contains_item(self) -> None:
        """Test contains operator."""
        nodes = Nodes(self.pyvlx)
        window1 = Window(self.pyvlx, 23, "Window_1", "aa:bb:aa:bb:aa:bb:aa:23")
        nodes.add(window1)
        window2 = Window(self.pyvlx, 42, "Window_2", "aa:bb:aa:bb:aa:bb:aa:42")  # not added
        self.assertTrue("Window_1" in nodes)
        self.assertTrue(23 in nodes)
        self.assertTrue(window1 in nodes)
        self.assertFalse("Window_2" in nodes)
        self.assertFalse(42 in nodes)
        self.assertFalse(window2 in nodes)

    def test_iter(self) -> None:
        """Test iterator."""
        nodes = Nodes(self.pyvlx)
        window1 = Window(self.pyvlx, 0, "Window_1", "aa:bb:aa:bb:aa:bb:aa:00")
        nodes.add(window1)
        window2 = Window(self.pyvlx, 1, "Window_2", "aa:bb:aa:bb:aa:bb:aa:01")
        nodes.add(window2)
        window3 = Window(self.pyvlx, 2, "Window_3", "aa:bb:aa:bb:aa:bb:aa:02")
        nodes.add(window3)
        self.assertEqual(tuple(nodes.__iter__()), (window1, window2, window3))  # pylint: disable=unnecessary-dunder-call

    def test_len(self) -> None:
        """Test len."""
        nodes = Nodes(self.pyvlx)
        self.assertEqual(len(nodes), 0)
        nodes.add(Window(self.pyvlx, 0, "Window_1", "aa:bb:aa:bb:aa:bb:aa:00"))
        nodes.add(Window(self.pyvlx, 1, "Window_2", "aa:bb:aa:bb:aa:bb:aa:01"))
        nodes.add(Window(self.pyvlx, 2, "Window_3", "aa:bb:aa:bb:aa:bb:aa:02"))
        nodes.add(Window(self.pyvlx, 3, "Window_4", "aa:bb:aa:bb:aa:bb:aa:03"))
        self.assertEqual(len(nodes), 4)

    def test_add_same_object(self) -> None:
        """Test adding object with same node_id."""
        nodes = Nodes(self.pyvlx)
        self.assertEqual(len(nodes), 0)
        nodes.add(Window(self.pyvlx, 0, "Window_1", "aa:bb:aa:bb:aa:bb:aa:00"))
        nodes.add(Window(self.pyvlx, 1, "Window_2", "aa:bb:aa:bb:aa:bb:aa:01"))
        nodes.add(Window(self.pyvlx, 2, "Window_3", "aa:bb:aa:bb:aa:bb:aa:02"))
        nodes.add(Window(self.pyvlx, 1, "Window_2_same_id", "aa:bb:aa:bb:aa:bb:aa:01"))
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].name, "Window_2_same_id")

    def test_add_item_failed(self) -> None:
        """Test add() with wrong type."""
        nodes = Nodes(self.pyvlx)
        with self.assertRaises(TypeError):
            nodes.add(nodes)  # type: ignore
        with self.assertRaises(TypeError):
            nodes.add("device")  # type: ignore

    def test_clear(self) -> None:
        """Test clear() method."""
        nodes = Nodes(self.pyvlx)
        self.assertEqual(len(nodes), 0)
        node_1 = Window(self.pyvlx, 0, "Window_1", "aa:bb:aa:bb:aa:bb:aa:00")
        node_2 = Window(self.pyvlx, 1, "Window_2", "aa:bb:aa:bb:aa:bb:aa:01")
        nodes.add(node_1)
        nodes.add(node_2)

        self.pyvlx.connection.unregister_connection_opened_cb.reset_mock()
        self.pyvlx.connection.unregister_connection_closed_cb.reset_mock()

        nodes.clear()

        self.pyvlx.connection.unregister_connection_opened_cb.assert_any_call(node_1.after_update)
        self.pyvlx.connection.unregister_connection_opened_cb.assert_any_call(node_2.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_any_call(node_1.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_any_call(node_2.after_update)
        self.assertEqual(len(nodes), 0)

    def test_add_replaces_node_and_disposes_old(self) -> None:
        """Test replacing a node unregisters callbacks on the old instance."""
        nodes = Nodes(self.pyvlx)
        node_1 = Window(self.pyvlx, 1, "Window_1", "aa:bb:aa:bb:aa:bb:aa:01")
        node_1_replacement = Window(self.pyvlx, 1, "Window_1_new", "aa:bb:aa:bb:aa:bb:aa:01")
        nodes.add(node_1)

        self.pyvlx.connection.unregister_connection_opened_cb.reset_mock()
        self.pyvlx.connection.unregister_connection_closed_cb.reset_mock()

        nodes.add(node_1_replacement)

        self.pyvlx.connection.unregister_connection_opened_cb.assert_called_once_with(node_1.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_called_once_with(node_1.after_update)
        self.assertIs(nodes[1], node_1_replacement)

    def test_node_str(self) -> None:
        """Test string representation of node."""
        node = Node(
            pyvlx=self.pyvlx,
            node_id=23,
            name="Test Abstract Node",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        node.last_frame_state = OperatingState.EXECUTING
        node.last_frame_status_reply = StatusReply.BATTERY_LEVEL
        self.assertEqual(
            str(node),
            '<Node name="Test Abstract Node" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" '
            'last_frame_state="OperatingState.EXECUTING" last_frame_status_reply="StatusReply.BATTERY_LEVEL"/>',
        )

    def test_node_represents_same_node(self) -> None:
        """Test identity comparison helper on Node."""
        with_serial_a = Node(self.pyvlx, 1, "A", "aa:bb:aa:bb:aa:bb:aa:01")
        with_serial_b_same = Node(self.pyvlx, 2, "B", "aa:bb:aa:bb:aa:bb:aa:01")
        with_serial_c_other = Node(self.pyvlx, 1, "C", "aa:bb:aa:bb:aa:bb:aa:99")
        no_serial_same_id = Node(self.pyvlx, 1, "D", None)
        no_serial_other_id = Node(self.pyvlx, 2, "E", None)

        self.assertTrue(with_serial_a.represents_same_node(with_serial_b_same))
        self.assertFalse(with_serial_a.represents_same_node(with_serial_c_other))
        self.assertFalse(with_serial_a.represents_same_node(no_serial_same_id))
        self.assertTrue(no_serial_same_id.represents_same_node(Node(self.pyvlx, 1, "F", None)))
        self.assertFalse(no_serial_same_id.represents_same_node(no_serial_other_id))

        window = Window(self.pyvlx, 3, "W", "aa:bb:aa:bb:aa:bb:aa:03")
        blind = Blind(self.pyvlx, 4, "B", "aa:bb:aa:bb:aa:bb:aa:03")
        self.assertFalse(window.represents_same_node(blind))


class TestNodesReload(unittest.TestCase):
    """Tests for _load_all_nodes merge behavior."""

    def setUp(self) -> None:
        """Set up TestNodesReload."""
        self.pyvlx = MagicMock(spec=PyVLX)
        connection = MagicMock(spec=Connection)
        self.pyvlx.attach_mock(mock=connection, attribute="connection")

    def _mock_get_all_nodes_information(self) -> MagicMock:
        event = MagicMock()
        event.success = True
        event.notification_frames = [object()]
        event.do_api_call = AsyncMock()
        return event

    def test_load_all_nodes_keeps_existing_node_when_serial_matches(self) -> None:
        """Existing node object should be kept when serial_number matches."""
        nodes = Nodes(self.pyvlx)
        existing = Window(self.pyvlx, 1, "Old name", "aa:bb:aa:bb:aa:bb:aa:01")
        existing.last_frame_state = OperatingState.EXECUTING
        callback = AsyncMock()
        existing.register_device_updated_cb(callback)
        nodes.add(existing)

        loaded = Window(self.pyvlx, 9, "New name", "aa:bb:aa:bb:aa:bb:aa:01")

        get_all_nodes_information = self._mock_get_all_nodes_information()
        with patch("pyvlx.nodes.GetAllNodesInformation", return_value=get_all_nodes_information), patch(
            "pyvlx.nodes.convert_frame_to_node", return_value=loaded
        ):
            asyncio.run(nodes._load_all_nodes())  # pylint: disable=W0212

        self.assertIs(nodes[9], existing)
        self.assertEqual(existing.name, "New name")
        self.assertEqual(existing.last_frame_state, OperatingState.EXECUTING)
        self.assertIn(callback, existing.device_updated_cbs)
        self.assertFalse(existing._disposed)  # pylint: disable=protected-access

        self.pyvlx.connection.unregister_connection_opened_cb.assert_called_once_with(loaded.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_called_once_with(loaded.after_update)

        # The temporary loaded object is disposed because existing was kept.
        self.pyvlx.connection.register_connection_opened_cb.assert_any_call(existing.after_update)
        self.pyvlx.connection.register_connection_closed_cb.assert_any_call(existing.after_update)

    def test_load_all_nodes_disposes_removed_nodes(self) -> None:
        """Nodes no longer present in the snapshot should be disposed."""
        nodes = Nodes(self.pyvlx)
        removed = Window(self.pyvlx, 1, "Removed", "aa:bb:aa:bb:aa:bb:aa:01")
        nodes.add(removed)

        loaded = Window(self.pyvlx, 2, "New", "aa:bb:aa:bb:aa:bb:aa:02")
        get_all_nodes_information = self._mock_get_all_nodes_information()
        with patch("pyvlx.nodes.GetAllNodesInformation", return_value=get_all_nodes_information), patch(
            "pyvlx.nodes.convert_frame_to_node", return_value=loaded
        ):
            asyncio.run(nodes._load_all_nodes())  # pylint: disable=W0212

        self.assertEqual(len(nodes), 1)
        self.assertIs(nodes[2], loaded)
        self.pyvlx.connection.unregister_connection_opened_cb.assert_any_call(removed.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_any_call(removed.after_update)

    def test_load_all_nodes_does_not_match_by_node_id_if_only_one_serial_exists(self) -> None:
        """Node_id fallback is only valid when both serial numbers are missing."""
        nodes = Nodes(self.pyvlx)
        existing = Window(self.pyvlx, 1, "Existing", "aa:bb:aa:bb:aa:bb:aa:01")
        existing.last_frame_state = OperatingState.EXECUTING
        nodes.add(existing)

        loaded = Window(self.pyvlx, 1, "Loaded", None)
        get_all_nodes_information = self._mock_get_all_nodes_information()
        with patch("pyvlx.nodes.GetAllNodesInformation", return_value=get_all_nodes_information), patch(
            "pyvlx.nodes.convert_frame_to_node", return_value=loaded
        ):
            asyncio.run(nodes._load_all_nodes())  # pylint: disable=W0212

        self.assertIs(nodes[1], loaded)
        self.assertIsNone(loaded.last_frame_state)
        self.pyvlx.connection.unregister_connection_opened_cb.assert_any_call(existing.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_any_call(existing.after_update)

    def test_load_all_nodes_replaces_when_type_differs_even_with_same_serial(self) -> None:
        """Type mismatch prevents identity match and replaces existing instance."""
        nodes = Nodes(self.pyvlx)
        existing = Window(self.pyvlx, 1, "Window", "aa:bb:aa:bb:aa:bb:aa:01")
        nodes.add(existing)

        loaded = Blind(self.pyvlx, 7, "Blind", "aa:bb:aa:bb:aa:bb:aa:01")
        get_all_nodes_information = self._mock_get_all_nodes_information()
        with patch("pyvlx.nodes.GetAllNodesInformation", return_value=get_all_nodes_information), patch(
            "pyvlx.nodes.convert_frame_to_node", return_value=loaded
        ):
            asyncio.run(nodes._load_all_nodes())  # pylint: disable=W0212

        self.assertIs(nodes[7], loaded)
        self.pyvlx.connection.unregister_connection_opened_cb.assert_any_call(existing.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_any_call(existing.after_update)


class TestNodesLoadNode(unittest.TestCase):
    """Tests asserting _load_node has the same identity-preserving behaviour as _load_all_nodes."""

    def setUp(self) -> None:
        """Set up TestNodesLoadNode."""
        self.pyvlx = MagicMock(spec=PyVLX)
        connection = MagicMock(spec=Connection)
        self.pyvlx.attach_mock(mock=connection, attribute="connection")

    def _mock_get_node_information(self, loaded: Node) -> MagicMock:  # pylint: disable=unused-argument
        event = MagicMock()
        event.success = True
        event.notification_frame = object()
        event.do_api_call = AsyncMock()
        return event

    def test_load_node_keeps_existing_instance_when_serial_matches(self) -> None:
        """load(node_id=…) must preserve the existing instance, just like load_all_nodes."""
        nodes = Nodes(self.pyvlx)
        existing = Window(self.pyvlx, 1, "Old name", "aa:bb:aa:bb:aa:bb:aa:01")
        callback = AsyncMock()
        existing.register_device_updated_cb(callback)
        nodes.add(existing)

        loaded = Window(self.pyvlx, 1, "New name", "aa:bb:aa:bb:aa:bb:aa:01")

        get_node_information = self._mock_get_node_information(loaded)
        with patch("pyvlx.nodes.GetNodeInformation", return_value=get_node_information), patch(
            "pyvlx.nodes.convert_frame_to_node", return_value=loaded
        ):
            asyncio.run(nodes._load_node(node_id=1))  # pylint: disable=protected-access

        self.assertIs(nodes[1], existing)
        self.assertEqual(existing.name, "New name")
        self.assertIn(callback, existing.device_updated_cbs)
        self.assertFalse(existing._disposed)  # pylint: disable=protected-access

        # Only the temporary loaded object should be unregistered, not the kept existing one.
        self.pyvlx.connection.unregister_connection_opened_cb.assert_called_once_with(loaded.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb.assert_called_once_with(loaded.after_update)
