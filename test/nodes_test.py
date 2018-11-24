"""Unit test for Nodes object."""
import unittest
from pyvlx import PyVLX, Nodes, Window, RollerShutter, Blind


# pylint: disable=too-many-public-methods,invalid-name

class TestNodes(unittest.TestCase):
    """Test class for nodes object."""

    def test_get_item(self):
        """Test get_item."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        window = Window(pyvlx, 0, 'Window')
        nodes.add(window)
        blind = Blind(pyvlx, 1, 'Blind')
        nodes.add(blind)
        roller_shutter = RollerShutter(pyvlx, 2, 'Roller Shutter')
        nodes.add(roller_shutter)
        self.assertEqual(nodes['Window'], window)
        self.assertEqual(nodes['Blind'], blind)
        self.assertEqual(nodes['Roller Shutter'], roller_shutter)
        self.assertEqual(nodes[0], window)
        self.assertEqual(nodes[1], blind)
        self.assertEqual(nodes[2], roller_shutter)

    def test_get_item_failed(self):
        """Test get_item with non existing object."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        window1 = Window(pyvlx, 0, 'Window_1')
        nodes.add(window1)
        with self.assertRaises(KeyError):
            nodes['Window_2']  # pylint: disable=pointless-statement
        with self.assertRaises(IndexError):
            nodes[1]  # pylint: disable=pointless-statement

    def test_iter(self):
        """Test iterator."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        window1 = Window(pyvlx, 0, 'Window_1')
        nodes.add(window1)
        window2 = Window(pyvlx, 1, 'Window_2')
        nodes.add(window2)
        window3 = Window(pyvlx, 2, 'Window_3')
        nodes.add(window3)
        self.assertEqual(
            tuple(nodes.__iter__()),
            (window1, window2, window3))

    def test_len(self):
        """Test len."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        self.assertEqual(len(nodes), 0)
        nodes.add(Window(pyvlx, 0, 'Window_1'))
        nodes.add(Window(pyvlx, 1, 'Window_2'))
        nodes.add(Window(pyvlx, 2, 'Window_3'))
        nodes.add(Window(pyvlx, 3, 'Window_4'))
        self.assertEqual(len(nodes), 4)

    def test_add_same_object(self):
        """Test adding object with same node_id."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        self.assertEqual(len(nodes), 0)
        nodes.add(Window(pyvlx, 0, 'Window_1'))
        nodes.add(Window(pyvlx, 1, 'Window_2'))
        nodes.add(Window(pyvlx, 2, 'Window_3'))
        nodes.add(Window(pyvlx, 1, 'Window_2_same_id'))
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].name, 'Window_2_same_id')

    def test_add_item_failed(self):
        """Test add() with wrong type."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        with self.assertRaises(TypeError):
            nodes.add(nodes)
        with self.assertRaises(TypeError):
            nodes.add("device")

    def test_clear(self):
        """Test clear() method."""
        pyvlx = PyVLX()
        nodes = Nodes(pyvlx)
        self.assertEqual(len(nodes), 0)
        nodes.add(Window(pyvlx, 0, 'Window_1'))
        nodes.add(Window(pyvlx, 1, 'Window_2'))
        nodes.clear()
        self.assertEqual(len(nodes), 0)
