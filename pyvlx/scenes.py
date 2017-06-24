import json
from .scene import Scene

class Scenes:

    def __init__(self, pyvlx):
        self.pyvlx = pyvlx
        self.__scenes = []


    def __iter__(self):
        yield from self.__scenes


    def __getitem__(self, key):
        for scene in self.__scenes:
            if scene.name == key:
                return scene

        if isinstance(key, int):
            return self.__scenes[key]
        raise KeyError


    def __len__(self):
        return len(self.__scenes)


    def add(self, scene):
        if not isinstance(scene, Scene):
            raise TypeError()
        self.__scenes.append(scene)


    async def load(self):
        json_response = await self.pyvlx.interface.api_call('scenes', 'get')
        if not 'data' in json_response:
            raise Exception('no element data found in response: {0}'.format(json.dumps(json_response)))
        data = json_response['data']

        for item in data:
            self.load_scene(item)


    def load_scene(self, item):
        scene = Scene.from_config(self.pyvlx, item)
        self.add(scene)
