"""Unit test for roller shutter."""

import unittest
import asyncio

from pyvlx import PyVLX, Window


# pylint: disable=too-many-public-methods,invalid-name
class TestWindow(unittest.TestCase):
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
        window = Window(pyvlx, 0, 'Test Window', 0, 2)
        self.assertEqual(window.get_name(), "Test Window")

    def test_str(self):
        pyvlx = PyVLX()
        window = Window(pyvlx, 0, 'Test Window', 0, 2)
        self.assertEqual(
            str(window),
            '<Window name="Test Window" id="0" subtype="0" ' \
            'typeId="2" />')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestWindow)
unittest.TextTestRunner(verbosity=2).run(SUITE)
