from .const import Command
from .frame import FrameBase


class FrameCommandSendRequest(FrameBase):
    """Frame for sending command to gw."""

    def __init__(self, node_ids=None, position=None, session_id=None):
        """Init Frame."""
        super().__init__(Command.GW_COMMAND_SEND_REQ)
        self.node_ids = node_ids
        self.position = position
        self.session_id = session_id

    def get_payload(self):
        """Return Payload."""
        # Session id
        ret = bytes([self.session_id >> 8 & 255, self.session_id & 255])
        # Originator
        ret += bytes([1])
        # Priority
        ret += bytes([3])
        # Parameter active
        ret += bytes([0]) # parameter active
        # FPI 1+2
        ret += bytes([0])
        ret += bytes([0])
        # Main parameter + functional parameter (in our case: position)
        ret += bytes([self.position*2,0])
        ret += bytes(32)
        # Nodes array: Number of nodes + node array + padding
        ret += bytes([len(self.node_ids)]) # index array count (wieviele indexes)
        ret += bytes(self.node_ids) + bytes(20-len(self.node_ids))
        # Pririty Level Lock
        ret += bytes([0])
        # PLI 1+2
        ret += bytes([0,0]) 
        # Locktime
        ret += bytes([0])
        return ret

    def from_payload(self, payload):
        """Init frame from binary data."""
        if len(payload) != 66:
            raise PyVLXException("FrameCommandSendRequest_has_invalid_payload_length")
        self.session_id = payload[0]*256 + payload[1]
        
        len_node_ids = payload[41]
        if len_node_ids > 20:
            raise PyVLXException("FrameCommandSendRequest_has_invalid_node_id_length")
        self.node_ids = []
        for i in range(len_node_ids):
            self.node_ids.append(payload[42] + i)
        self.position = int(payload[7]/2)
        if self.position > 100:
            raise PyVLXException("FrameCommandSendRequest_has_invalid_position")
        pass

    def __str__(self):
        """Return human readable string."""
        return '<FrameCommandSendRequest node_ids={} position={} session_id={}/>'.format(self.node_ids, self.position, self.session_id) 
