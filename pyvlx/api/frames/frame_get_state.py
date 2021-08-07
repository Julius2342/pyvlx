"""Frames for receiving state from gateway."""
from pyvlx.const import Command, GatewayState, GatewaySubState

from .frame import FrameBase


class FrameGetStateRequest(FrameBase):
    """Frame for requesting state."""

    PAYLOAD_LEN = 0

    def __init__(self):
        """Init Frame."""
        super().__init__(Command.GW_GET_STATE_REQ)


class FrameGetStateConfirmation(FrameBase):
    """Frame for confirmation for get state requests."""

    PAYLOAD_LEN = 6

    def __init__(
            self,
            gateway_state=GatewayState.TEST_MODE,
            gateway_sub_state=GatewaySubState.IDLE,
    ):
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
        return '<{} gateway_state="{}" gateway_sub_state="{}"/>'.format(
            type(self).__name__, self.gateway_state, self.gateway_sub_state
        )
