"""Unit test for scene."""

import unittest
from pyvlx import PyVLX
from pyvlx.scene import Scene


# pylint: disable=too-many-public-methods,invalid-name
class TestScene(unittest.TestCase):
    """Test class for scene."""

    def test_get_name(self):
        """Test get_name()."""
        pyvlx = PyVLX()
        scene = Scene(pyvlx, 2, 'Scene 1')
        self.assertEqual(scene.name, "Scene 1")
        self.assertEqual(scene.scene_id, 2)

    def test_str(self):
        """Test string representation of Scene object."""
        pyvlx = PyVLX()
        scene = Scene(pyvlx, 2, 'Scene 1')
        self.assertEqual(
            str(scene),
            '<Scene name="Scene 1" id="2" />')
