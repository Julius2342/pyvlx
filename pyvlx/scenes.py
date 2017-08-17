"""Module for storing scenes."""

import json
from .scene import Scene
from .exception import PyVLXException


class Scenes:
    """Object for storing scenes."""

    def __init__(self, pyvlx):
        """Initialize Scenes class."""
        self.pyvlx = pyvlx
        self.__scenes = []

    def __iter__(self):
        """Iterator."""
        yield from self.__scenes

    def __getitem__(self, key):
        """Return scene by name or by index."""
        for scene in self.__scenes:
            if scene.name == key:
                return scene
        if isinstance(key, int):
            return self.__scenes[key]
        raise KeyError

    def __len__(self):
        """Return number of scenes."""
        return len(self.__scenes)

    def add(self, scene):
        """Add scene."""
        if not isinstance(scene, Scene):
            raise TypeError()
        self.__scenes.append(scene)

    async def load(self):
        """Load scenes from KLF 200."""
        json_response = await self.pyvlx.interface.api_call('scenes', 'get')
        self.data_import(json_response)

    def data_import(self, json_response):
        """Import scenes from JSON response."""
        if 'data' not in json_response:
            raise PyVLXException('no element data found: {0}'.format(
                json.dumps(json_response)))
        data = json_response['data']
        for item in data:
            self.load_scene(item)

    def load_scene(self, item):
        """Load scene from json."""
        scene = Scene.from_config(self.pyvlx, item)
        self.add(scene)
