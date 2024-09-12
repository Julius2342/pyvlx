"""Unit test for Nodes object."""
import unittest
from unittest.mock import MagicMock

from pyvlx import Blind, Nodes, PyVLX, RollerShutter, Window
from pyvlx.node import Node

# pylint: disable=too-many-public-methods,invalid-name


class TestNodes(unittest.TestCase):
    """Test class for nodes object."""

    def setUp(self) -> None:
        """Set up TestNodes."""
        self.pyvlx = MagicMock(spec=PyVLX)

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
        nodes.add(Window(self.pyvlx, 0, "Window_1", "aa:bb:aa:bb:aa:bb:aa:00"))
        nodes.add(Window(self.pyvlx, 1, "Window_2", "aa:bb:aa:bb:aa:bb:aa:01"))
        nodes.clear()
        self.assertEqual(len(nodes), 0)

    def test_node_str(self) -> None:
        """Test string representation of node."""
        node = Node(
            pyvlx=self.pyvlx,
            node_id=23,
            name="Test Abstract Node",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        self.assertEqual(
            str(node),
            '<Node name="Test Abstract Node" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23"/>',
        )
