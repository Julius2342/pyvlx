"""Unit test for roller shutter."""

import unittest
import asyncio

from pyvlx import PyVLX, RollerShutter


# pylint: disable=too-many-public-methods,invalid-name
class TestDevices(unittest.TestCase):
    """Test class for roller shutter."""

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
        rollershutter = RollerShutter(pyvlx, 0, 'Test Shutter', 0, 2)
        self.assertEqual(rollershutter.get_name(), "Test Shutter")

    def test_str(self):
        """Test string representation of RollerShutter objec."""
        pyvlx = PyVLX()
        rollershutter = RollerShutter(pyvlx, 0, 'Test Shutter', 0, 2)
        self.assertEqual(
            str(rollershutter),
            '<RollerShutter name="Test Shutter" id="0" subtype="0" '
            'typeId="2" />')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevices)
unittest.TextTestRunner(verbosity=2).run(SUITE)
