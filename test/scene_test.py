"""Unit test for roller shutter."""

import unittest
import asyncio

from pyvlx import PyVLX, Scene


# pylint: disable=too-many-public-methods,invalid-name
class TestScene(unittest.TestCase):
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
        scene = Scene(pyvlx, 2, 'Scene 1')
        self.assertEqual(scene.get_name(), "Scene 1")

    def test_str(self):
        """Test string representation of Scene object."""
        pyvlx = PyVLX()
        scene = Scene(pyvlx, 2, 'Scene 1')
        self.assertEqual(
            str(scene),
            '<Scene name="Scene 1" id="2" />')


SUITE = unittest.TestLoader().loadTestsFromTestCase(TestScene)
unittest.TextTestRunner(verbosity=2).run(SUITE)
