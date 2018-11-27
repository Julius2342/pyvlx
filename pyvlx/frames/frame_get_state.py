"""Frames for receiving state from gateway."""
from enum import Enum

from pyvlx.const import Command

from .frame import FrameBase


class FrameGetStateRequest(FrameBase):
    """Frame for requesting state."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_STATE_REQ)


class GatewayState(Enum):
    """Enum class for status if gateway."""

    TEST_MODE = 0
    GATEWAY_MODE_NO_ACTUATOR = 1
    GATEWAY_MODE_WITH_ACTUATORS = 2
    BEACON_MODE_NOT_CONFIGURED = 3
    BEACON_MODE_CONFIGURED = 4


class GatewaySubState(Enum):
    """Enum class for substate if gateway."""

    IDLE = 0x00
    PERFORMING_TASK_CONFIGURATION_SERVICE_HANDLER = 0x01
    PERFORMING_TASK_SCENE_CONFIGURATION = 0x02
    PERFORMING_TASK_INFORMATION_SERVICE_CONFIGURATION = 0x03
    PERFORMING_TASK_CONTACT_INPUT_CONFIGURATION = 0x04
    PERFORMING_TASK_COMMAND = 0x80
    PERFORMING_TASK_ACTIVATE_GROUP = 0x81
    PERFORMING_TASK_ACTIVATE_SCENE = 0x82


class FrameGetStateConfirmation(FrameBase):
    """Frame for confirmation for get state requests."""

    PAYLOAD_LEN = 6

    def __init__(self, gateway_state=GatewayState.TEST_MODE, gateway_sub_state=GatewaySubState.IDLE):
        """Init Frame."""
        super().__init__(Command.GW_GET_STATE_CFM)
        self.gateway_state = gateway_state
        self.gateway_sub_state = gateway_sub_state

    def get_payload(self):
        """Return Payload."""
        payload = bytes([self.gateway_state.value, self.gateway_sub_state.value])
        payload += bytes(4)  # State date, reserved for future use
        return payload

    def from_payload(self, payload):
        """Init frame from binary data."""
        self.gateway_state = GatewayState(payload[0])
        self.gateway_sub_state = GatewaySubState(payload[1])

    def __str__(self):
        """Return human readable string."""
        return '<FrameGetStateConfirmation gateway_state="{}" gateway_sub_state="{}"/>'.format(self.gateway_state, self.gateway_sub_state)
