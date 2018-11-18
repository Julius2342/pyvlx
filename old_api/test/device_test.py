"""Unit test for device class."""

import unittest
import asyncio

from pyvlx import PyVLX, Device


# pylint: disable=too-many-public-methods,invalid-name
class TestDevice(unittest.TestCase):
    """Test class for devices container."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_name(self):
        """Test name."""
        pyvlx = PyVLX()
        device = Device(pyvlx, 0, "TestDevice")
        self.assertEqual(device.get_name(), "TestDevice")


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestDevice)
unittest.TextTestRunner(verbosity=2).run(SUITE)
