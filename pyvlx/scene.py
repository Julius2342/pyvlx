"""Module for scene."""
from pyvlx.activate_scene import ActivateScene


class Scene:
    """Object for scene."""

    # pylint: disable=too-few-public-methods

    def __init__(self, pyvlx, scene_id, name):
        """Initialize Scene object."""
        self.pyvlx = pyvlx
        self.scene_id = scene_id
        self.name = name

    async def run(self):
        """Run scene."""
        activate_scene = ActivateScene(connection=self.pyvlx.connection, scene_id=self.scene_id)
        await activate_scene.do_api_call()

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
