"""Unit test for roller shutter."""
import unittest

from pyvlx import Blade, Blind, PyVLX, RollerShutter, Window, Awning, Parameter


# pylint: disable=too-many-public-methods,invalid-name
class TestOpeningDevice(unittest.TestCase):
    """Test class for roller shutter."""

    def test_window_str(self):
        """Test string representation of Window object."""
        pyvlx = PyVLX()
        window = Window(pyvlx=pyvlx, node_id=23, name='Test Window', rain_sensor=True, serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        self.assertEqual(str(window),
                         '<Window name="Test Window" node_id="23" rain_sensor=True serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>')

    def test_blind_str(self):
        """Test string representation of Blind object."""
        pyvlx = PyVLX()
        blind = Blind(pyvlx=pyvlx, node_id=23, name='Test Blind', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        self.assertEqual(str(blind), '<Blind name="Test Blind" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>')

    def test_roller_shutter_str(self):
        """Test string representation of RolllerShutter object."""
        pyvlx = PyVLX()
        roller_shutter = RollerShutter(pyvlx=pyvlx, node_id=23, name='Test Roller Shutter', serial_number='aa:bb:aa:bb:aa:bb:aa:23',
                                       position_parameter=Parameter(Parameter.from_int(int(0.97*Parameter.MAX))))
        self.assertEqual(str(roller_shutter),
                         '<RollerShutter name="Test Roller Shutter" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="97 %"/>')

    def test_blade_str(self):
        """Test string representation of Blade object."""
        pyvlx = PyVLX()
        blade = Blade(pyvlx=pyvlx, node_id=23, name='Test Blade', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        self.assertEqual(str(blade), '<Blade name="Test Blade" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>')

    def test_awning_str(self):
        """Test string representation of Awning object."""
        pyvlx = PyVLX()
        awning = Awning(pyvlx=pyvlx, node_id=23, name='Test Awning', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        self.assertEqual(str(awning), '<Awning name="Test Awning" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23" position="UNKNOWN"/>')

    def test_eq(self):
        """Testing eq method with positive results."""
        pyvlx = PyVLX()
        node1 = Blind(pyvlx=pyvlx, node_id=23, name='xxx', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        node2 = Blind(pyvlx=pyvlx, node_id=23, name='xxx', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        self.assertEqual(node1, node2)

    def test_nq(self):
        """Testing eq method with negative results."""
        pyvlx = PyVLX()
        node1 = Blind(pyvlx=pyvlx, node_id=23, name='xxx', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        node2 = Blind(pyvlx=pyvlx, node_id=24, name='xxx', serial_number='aa:bb:aa:bb:aa:bb:aa:24')
        node3 = RollerShutter(pyvlx=pyvlx, node_id=23, name='xxx', serial_number='aa:bb:aa:bb:aa:bb:aa:23')
        self.assertNotEqual(node1, node2)
        self.assertNotEqual(node2, node3)
        self.assertNotEqual(node3, node1)
