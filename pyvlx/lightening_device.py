"""Module for lights."""
from typing import TYPE_CHECKING, Optional

from .api import CommandSend
from .node import Node
from .parameter import Intensity

if TYPE_CHECKING:
    from pyvlx import PyVLX


class LighteningDevice(Node):
    """Meta class for turning on device with one main parameter for intensity."""

    def __init__(self, pyvlx: "PyVLX", node_id: int, name: str, serial_number: Optional[str]):
        """Initialize turning on device.

        Parameters:
            * pyvlx: PyVLX object
            * node_id: internal id for addressing nodes.
                Provided by KLF 200 device
            * name: node name
            * serial_number: serial number of the node.

        """
        super().__init__(
            pyvlx=pyvlx, node_id=node_id, name=name, serial_number=serial_number
        )
        self.intensity = Intensity()

    async def set_intensity(self, intensity: Intensity, wait_for_completion: bool = True) -> None:
        """Set light to desired intensity.

        Parameters:
            * intensity: Intensity object containing the target intensity.
            * wait_for_completion: If set, function will return
                after device has reached target intensity.

        """
        command = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=intensity,
        )
        await command.send()
        await self.after_update()

    async def turn_on(self, wait_for_completion: bool = True) -> None:
        """Turn on light.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target intensity.

        """
        await self.set_intensity(
            intensity=Intensity(intensity_percent=0),
            wait_for_completion=wait_for_completion,
        )

    async def turn_off(self, wait_for_completion: bool = True) -> None:
        """Turn off light.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target intensity.

        """
        await self.set_intensity(
            intensity=Intensity(intensity_percent=100),
            wait_for_completion=wait_for_completion,
        )

    def __str__(self) -> str:
        """Return object as readable string."""
        return (
            '<{} name="{}" '
            'node_id="{}" '
            'serial_number="{}"/>'.format(
                type(self).__name__, self.name, self.node_id, self.serial_number
            )
        )


class Light(LighteningDevice):
    """Lights that support setting brightness."""


class OnOffLight(LighteningDevice):
    """Lights supporting on/off only.

    Note:
        This class inherits :meth:`set_intensity` from :class:`LighteningDevice`,
        but the underlying hardware only supports binary on/off operation.
        Use :meth:`turn_on` and :meth:`turn_off` for normal control. Calling
        :meth:`set_intensity` with intermediate values may not have the expected
        effect and will typically be handled by the device as a simple on/off
        command.
    """
