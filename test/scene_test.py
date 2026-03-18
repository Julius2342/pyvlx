"""Unit test for scene."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from pyvlx import Scene


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


class TestSceneRun(unittest.IsolatedAsyncioTestCase):
    """Test class for Scene.run()."""

    @patch("pyvlx.scene.ActivateScene")
    async def test_run_forwards_timeout(self, mock_activate_scene: MagicMock) -> None:
        """Test run creates ActivateScene with the provided timeout."""
        pyvlx = MagicMock()
        scene = Scene(pyvlx, 2, "Scene 1")
        activate_scene_instance = MagicMock()
        activate_scene_instance.send = AsyncMock()
        mock_activate_scene.return_value = activate_scene_instance

        await scene.run(wait_for_completion=True, timeout_in_seconds=25)

        mock_activate_scene.assert_called_once_with(
            pyvlx=pyvlx,
            wait_for_completion=True,
            scene_id=2,
            timeout_in_seconds=25,
        )
        activate_scene_instance.send.assert_awaited_once()

    @patch("pyvlx.scene.ActivateScene")
    async def test_run_uses_default_timeout_when_not_provided(self, mock_activate_scene: MagicMock) -> None:
        """Test run creates ActivateScene with the default timeout."""
        pyvlx = MagicMock()
        scene = Scene(pyvlx, 2, "Scene 1")
        activate_scene_instance = MagicMock()
        activate_scene_instance.send = AsyncMock()
        mock_activate_scene.return_value = activate_scene_instance

        await scene.run(wait_for_completion=True)

        mock_activate_scene.assert_called_once_with(
            pyvlx=pyvlx,
            wait_for_completion=True,
            scene_id=2,
            timeout_in_seconds=60,
        )
        activate_scene_instance.send.assert_awaited_once()
