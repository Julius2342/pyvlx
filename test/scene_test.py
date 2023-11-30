"""Unit test for scene."""

import unittest
from unittest.mock import MagicMock

from pyvlx import Scene


# pylint: disable=too-many-public-methods,invalid-name
class TestScene(unittest.TestCase):
    """Test class for scene."""

    def test_get_name(self) -> None:
        """Test get_name()."""
        pyvlx = MagicMock()
        scene = Scene(pyvlx, 2, "Scene 1")
        self.assertEqual(scene.name, "Scene 1")
        self.assertEqual(scene.scene_id, 2)

    def test_str(self) -> None:
        """Test string representation of Scene object."""
        pyvlx = MagicMock()
        scene = Scene(pyvlx, 2, "Scene 1")
        self.assertEqual(str(scene), '<Scene name="Scene 1" id="2"/>')
