"""Module for lights."""
from .command_send import CommandSend
from .exception import PyVLXException
from .node import Node
from .parameter import Intensity


class LighteningDevice(Node):
    """Meta class for turning on device with one main parameter for intensity."""

    def __init__(self, pyvlx, node_id, name, serial_number):
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

    async def set_intensity(self, intensity, wait_for_completion=True):
        """Set light to desired intensity.

        Parameters:
            * intensity: Intensity object containing the target intensity.
            * wait_for_completion: If set, function will return
                after device has reached target intensity.

        """
        command_send = CommandSend(
            pyvlx=self.pyvlx,
            wait_for_completion=wait_for_completion,
            node_id=self.node_id,
            parameter=intensity,
        )
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        await self.after_update()

    async def turn_on(self, wait_for_completion=True):
        """Turn on light.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target intensity.

        """
        await self.set_intensity(
            intensity=Intensity(intensity_percent=0),
            wait_for_completion=wait_for_completion,
        )

    async def turn_off(self, wait_for_completion=True):
        """Turn off light.

        Parameters:
            * wait_for_completion: If set, function will return
                after device has reached target intensity.

        """
        await self.set_intensity(
            intensity=Intensity(intensity_percent=100),
            wait_for_completion=wait_for_completion,
        )


class Light(LighteningDevice):
    """Light object."""

    def __init__(self, pyvlx, node_id, name, serial_number):
        """Initialize Light class.

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

    def __str__(self):
        """Return object as readable string."""
        return (
            '<{} name="{}" '
            'node_id="{}" '
            'serial_number="{}"/>'.format(
                type(self).__name__, self.name, self.node_id, self.serial_number
            )
        )
