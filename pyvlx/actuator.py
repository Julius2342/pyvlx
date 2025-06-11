"""Module for Actuator known by KLF200."""
from math import floor

from pyvlx.const import (
    Manufactor, NodeType, NodeTypeWithSubtype, PowerMode, TurnAround)


class Actuator() :
    """Frame for confirmation for get network setup requests."""

    # pylint: disable-next=too-many-positional-arguments
    def __init__(self, idx: int = -1, address : bytes = bytes(3), subtype: NodeTypeWithSubtype = NodeTypeWithSubtype.NO_TYPE,
                 power_save_mode: PowerMode = PowerMode.ALWAYS_ALIVE, io: bool = False, rf: bool = False,
                 turn_around_time : TurnAround = TurnAround.NONE, manufactor: Manufactor = Manufactor.NONE, backbone : bytes = bytes(3)) :
        """Create a new instance of Actuator."""
        self.idx = idx
        self.address = address
        self.subtype = subtype
        self.power_save_mode = power_save_mode
        self.io = io
        self.rf = rf
        self.turn_around_time = turn_around_time
        self.manufactor = manufactor
        self.backbone = backbone

    def __str__(self) -> str:
        """Return human readable string."""
        return '<Actuator index="{}" address="{}" type="{}" subtype="{}" powerSaveMode="{}" io="{}" rf="{}"'\
               ' turnAroundTime="{}" manufactor="{}" backbone="{}"/>'.format(self.idx,
                                                                             ".".join(str(c) for c in self.address),
                                                                             self.get_node_type().name,
                                                                             self.subtype.name,
                                                                             self.power_save_mode.name,
                                                                             'true' if self.io else 'false',
                                                                             'true' if self.rf else 'false',
                                                                             self.turn_around_time.name,
                                                                             self.manufactor.name,
                                                                             ".".join(str(c) for c in self.backbone))

    def get_node_type(self) -> NodeType:
        """Return actuator main type."""
        return NodeType(floor(self.subtype.value / 64))  # 10 bits for Node type, 6 bits for Node subtype
