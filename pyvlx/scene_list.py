"""Module for retrieving scene list from API."""
from .scene import Scene
from .frame_get_scene_list import FrameGetSceneListRequest, FrameGetSceneListConfirmation, FrameGetSceneListNotification
from .api_event import ApiEvent


class SceneList(ApiEvent):
    """Class for retrieving scene list from API."""

    def __init__(self, pyvlx):
        """Initialize SceneList class."""
        super().__init__(pyvlx.connection)
        self.pyvlx = pyvlx
        self.success = False
        self.count_scenes = None
        self.__scenes = []

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetSceneListConfirmation):
            self.count_scenes = frame.count_scenes
            # We are still waiting for FrameGetSceneListNotification(s)
            return False
        if isinstance(frame, FrameGetSceneListNotification):
            self.add_scenes(frame.scenes)
            if frame.remaining_scenes != 0:
                # We are still waiting for FrameGetSceneListConfirmation(s)
                return False
            if self.count_scenes != len(self.__scenes):
                self.pyvlx.logger.warning("Warning: number of received scenes does not match expected number")
            self.success = True
            return True
        return False

    def add_scenes(self, scenes):
        """Adding scenes to internal scene array."""
        for scene in scenes:
            self.add(Scene(pyvlx=self.pyvlx, scene_id=scene[0], name=scene[1]))

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetSceneListRequest()

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
        await self.do_api_call()
