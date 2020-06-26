"""Unit test for lights."""
import unittest

from pyvlx import Light, PyVLX


# pylint: disable=too-many-public-methods,invalid-name
class TestLighteningDevice(unittest.TestCase):
    """Test class for lights."""

    def test_light_str(self):
        """Test string representation of Light object."""
        pyvlx = PyVLX()
        light = Light(
            pyvlx=pyvlx,
            node_id=23,
            name="Test Light",
            serial_number="aa:bb:aa:bb:aa:bb:aa:23",
        )
        self.assertEqual(
            str(light),
            '<Light name="Test Light" node_id="23" serial_number="aa:bb:aa:bb:aa:bb:aa:23"/>',
        )

    def test_eq(self):
        """Testing eq method with positive results."""
        pyvlx = PyVLX()
        node1 = Light(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        node2 = Light(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        self.assertEqual(node1, node2)

    def test_nq(self):
        """Testing eq method with negative results."""
        pyvlx = PyVLX()
        node1 = Light(
            pyvlx=pyvlx, node_id=23, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        node2 = Light(
            pyvlx=pyvlx, node_id=24, name="xxx", serial_number="aa:bb:aa:bb:aa:bb:aa:23"
        )
        self.assertNotEqual(node1, node2)
