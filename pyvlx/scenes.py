"""Module for storing and accessing scene list."""
from .exception import PyVLXException
from .get_scene_list import GetSceneList
from .scene import Scene


class Scenes():
    """Class for storing and accessing ."""

    def __init__(self, pyvlx):
        """Initialize Scenes class."""
        self.pyvlx = pyvlx
        self.__scenes = []

    def __iter__(self):
        """Iterator."""
        yield from self.__scenes

    def __getitem__(self, key):
        """Return scene by name or by index."""
        if isinstance(key, int):
            for scene in self.__scenes:
                if scene.scene_id == key:
                    return scene
        for scene in self.__scenes:
            if scene.name == key:
                return scene
        raise KeyError

    def __len__(self):
        """Return number of scenes."""
        return len(self.__scenes)

    def add(self, scene):
        """Add scene, replace existing scene if scene with scene_id is present."""
        if not isinstance(scene, Scene):
            raise TypeError()
        for i, j in enumerate(self.__scenes):
            if j.scene_id == scene.scene_id:
                self.__scenes[i] = scene
                return
        self.__scenes.append(scene)

    def clear(self):
        """Clear internal scenes array."""
        self.__scenes = []

    async def load(self):
        """Load scenes from KLF 200."""
        get_scene_list = GetSceneList(pyvlx=self.pyvlx)
        await get_scene_list.do_api_call()
        if not get_scene_list.success:
            raise PyVLXException("Unable to retrieve scene information")
        for scene in get_scene_list.scenes:
            self.add(Scene(pyvlx=self.pyvlx, scene_id=scene[0], name=scene[1]))
