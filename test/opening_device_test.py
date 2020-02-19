"""Unit test for roller shutter."""
import unittest

from pyvlx import Blind, PyVLX, RollerShutter, Window, Blade


# pylint: disable=too-many-public-methods,invalid-name
class TestOpeningDevice(unittest.TestCase):
    """Test class for roller shutter."""

    def test_window_str(self):
        """Test string representation of Window object."""
        pyvlx = PyVLX()
        window = Window(pyvlx=pyvlx, node_id=23, name='Test Window', rain_sensor=True)
        self.assertEqual(str(window), '<Window name="Test Window" node_id="23" rain_sensor=True/>')

    def test_blind_str(self):
        """Test string representation of Blind object."""
        pyvlx = PyVLX()
        blind = Blind(pyvlx=pyvlx, node_id=23, name='Test Blind')
        self.assertEqual(str(blind), '<Blind name="Test Blind" node_id="23"/>')

    def test_roller_shutter_str(self):
        """Test string representation of RolllerShutter object."""
        pyvlx = PyVLX()
        roller_shutter = RollerShutter(pyvlx=pyvlx, node_id=23, name='Test Roller Shutter')
        self.assertEqual(str(roller_shutter), '<RollerShutter name="Test Roller Shutter" node_id="23"/>')

    def test_blade_str(self):
        """Test string representation of Blade object."""
        pyvlx = PyVLX()
        blade = Blade(pyvlx=pyvlx, node_id=23, name='Test Blade')
        self.assertEqual(str(blade), '<Blade name="Test Blade" node_id="23"/>')

    def test_eq(self):
        """Testing eq method with positive results."""
        pyvlx = PyVLX()
        node1 = Blind(pyvlx=pyvlx, node_id=23, name='xxx')
        node2 = Blind(pyvlx=pyvlx, node_id=23, name='xxx')
        self.assertEqual(node1, node2)

    def test_nq(self):
        """Testing eq method with negative results."""
        pyvlx = PyVLX()
        node1 = Blind(pyvlx=pyvlx, node_id=23, name='xxx')
        node2 = Blind(pyvlx=pyvlx, node_id=24, name='xxx')
        node3 = RollerShutter(pyvlx=pyvlx, node_id=23, name='xxx')
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node1)
