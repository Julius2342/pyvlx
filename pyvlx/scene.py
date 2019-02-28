"""Module for scene."""
from .activate_scene import ActivateScene
from .exception import PyVLXException


class Scene:
    """Object for scene."""

    def __init__(self, pyvlx, scene_id, name):
        """Initialize Scene object.

        Parameters:
            * pyvlx: PyVLX object
            * scene_id: internal id for addressing scenes.
                Provided by KLF 200 device
            * name: scene name

        """
        self.pyvlx = pyvlx
        self.scene_id = scene_id
        self.name = name

    async def run(self, wait_for_completion=True):
        """Run scene.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target position.

        """
        activate_scene = ActivateScene(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            scene_id=self.scene_id)
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
