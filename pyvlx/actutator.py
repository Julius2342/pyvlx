"""
Module for Actutator known by KLF200

"""
from pyvlx.const import (Command, NodeTypeWithSubtype, PowerMode, TurnAround, Manufactor)

class Actutator() :
    """Frame for confirmation for get network setup requests."""
    def __init__(self, idx: bytes = bytes(1), address : bytes = bytes(3), actType: NodeTypeWithSubtype = NodeTypeWithSubtype.NO_TYPE,
                 powerSaveMode: PowerMode = PowerMode.ALWAYS_ALIVE, io: bool = False, rf: bool = False, turnAroundTime : TurnAround = TurnAround.none,
                 manufactor: Manufactor = Manufactor.none, backbone : bytes = bytes(3)) :
        self.idx = idx
        self.address = address
        self.type = actType
        self.powerSaveMode = powerSaveMode
        self.io = io
        self.rf = rf
        self.turnAroundTime = turnAroundTime
        self.manufactor = manufactor
        self.backbone = backbone
    def __str__(self) -> str:
        """Return human readable string."""
        return '<Actutator index="{}" address="{}" type="{}" powerSaveMode="{}" io="{}" rf="{}" turnAroundTime="{}" manufactor="{}" backbone="{}"/>'.format(
            self.idx,
            ".".join(str(c) for c in self.address),
            self.type.name,
            self.powerSaveMode.name,
            'true' if self.io else 'false',
            'true' if self.rf else 'false',
            self.turnAroundTime.name,
            self.manufactor.name,
            ".".join(str(c) for c in self.backbone)
        )
