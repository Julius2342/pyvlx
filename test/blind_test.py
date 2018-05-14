"""Unit test for blind."""

import unittest
import asyncio

from pyvlx import PyVLX, Blind


# pylint: disable=too-many-public-methods,invalid-name
class TestDevices(unittest.TestCase):
    """Test class for blind."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_get_name(self):
        """Test get_name()."""
        pyvlx = PyVLX()
        blind = Blind(pyvlx, 0, 'Test Blind', 0, 2)
        self.assertEqual(blind.get_name(), "Test Blind")

    def test_str(self):
        """Test string representation of Blind objec."""
        pyvlx = PyVLX()
        blind = Blind(pyvlx, 0, 'Test Blind', 0, 2)
        self.assertEqual(
            str(blind),
            '<Blind name="Test Blind" id="0" subtype="0" '
            'typeId="2" />')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevices)
unittest.TextTestRunner(verbosity=2).run(SUITE)
