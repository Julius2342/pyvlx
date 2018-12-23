"""Module for on/off switches."""
from .command_send import CommandSend
from .exception import PyVLXException
from .node import Node
from .parameter import SwitchParameter, SwitchParameterOff, SwitchParameterOn


class OnOffSwitch(Node):
    """Class for controlling on-off switches."""

    def __init__(self, pyvlx, node_id, name):
        """Initialize opening device."""
        super().__init__(pyvlx=pyvlx, node_id=node_id, name=name)
        self.parameter = SwitchParameter()

    async def set_state(self, parameter):
        """Set switch to desired state."""
        command_send = CommandSend(pyvlx=self.pyvlx, node_id=self.node_id, parameter=parameter)
        await command_send.do_api_call()
        if not command_send.success:
            raise PyVLXException("Unable to send command")
        self.parameter = parameter
        await self.after_update()

    async def set_on(self):
        """Set switch on."""
        await self.set_state(SwitchParameterOn())

    async def set_off(self):
        """Set switch off."""
        await self.set_state(SwitchParameterOff())

    def is_on(self):
        """Return if switch is set to on."""
        return self.parameter.is_on()

    def is_off(self):
        """Return if switch is set to off."""
        return self.parameter.is_off()
