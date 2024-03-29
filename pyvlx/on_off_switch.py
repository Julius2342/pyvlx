"""Module for on/off switches."""
from typing import TYPE_CHECKING, Optional

from .api.command_send import CommandSend
from .node import Node
from .parameter import SwitchParameter, SwitchParameterOff, SwitchParameterOn

if TYPE_CHECKING:
    from pyvlx import PyVLX


class OnOffSwitch(Node):
    """Class for controlling on-off switches."""

    def __init__(self, pyvlx: "PyVLX", node_id: int, name: str, serial_number: Optional[str]):
        """Initialize opening device."""
        super().__init__(
            pyvlx=pyvlx, node_id=node_id, name=name, serial_number=serial_number
        )
        self.parameter = SwitchParameter()

    async def set_state(self, parameter: SwitchParameter) -> None:
        """Set switch to desired state."""
        command = CommandSend(
            pyvlx=self.pyvlx, node_id=self.node_id, parameter=parameter
        )
        await command.send()
        await self.after_update()

    async def set_on(self) -> None:
        """Set switch on."""
        await self.set_state(SwitchParameterOn())

    async def set_off(self) -> None:
        """Set switch off."""
        await self.set_state(SwitchParameterOff())

    def is_on(self) -> bool:
        """Return if switch is set to on."""
        return self.parameter.is_on()

    def is_off(self) -> bool:
        """Return if switch is set to off."""
        return self.parameter.is_off()
