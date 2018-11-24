"""Module for scene."""
from .activate_scene import ActivateScene
from .exception import PyVLXException


class Scene:
    """Object for scene."""

    def __init__(self, pyvlx, scene_id, name):
        """Initialize Scene object."""
        self.pyvlx = pyvlx
        self.scene_id = scene_id
        self.name = name

    async def run(self):
        """Run scene."""
        activate_scene = ActivateScene(pyvlx=self.pyvlx, scene_id=self.scene_id)
        await activate_scene.do_api_call()
        if not activate_scene.success:
            raise PyVLXException("Unable to activate scene")

    def __str__(self):
        """Return object as readable string."""
        return '<Scene name="{0}" ' \
            'id="{1}" />' \
            .format(
                self.name,
                self.scene_id)

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
