"""
Module for basic object for nodes.

Node object is an interface class and should
be derived by other objects like window openers
and roller shutters.
"""
from typing import TYPE_CHECKING, Any, Awaitable, Callable, List, Optional

from .api import SetNodeName, WinkSend
from .const import OperatingState, RunStatus, StatusReply, WinkTime
from .exception import PyVLXException

if TYPE_CHECKING:
    from pyvlx import PyVLX

CallbackType = Callable[["Node"], Awaitable[None]]


class Node:
    """Class for node abstraction."""

    def __init__(self, pyvlx: "PyVLX", node_id: int, name: str, serial_number: Optional[str]):
        """Initialize Node object."""
        self.pyvlx = pyvlx
        self.node_id = node_id
        self.name = name
        self.serial_number = serial_number
        self.last_frame_state: Optional[OperatingState] = None
        self.last_frame_status_reply: Optional[StatusReply] = None
        self.last_frame_run_status: Optional[RunStatus] = None
        self.device_updated_cbs: List[CallbackType] = []
        self.pyvlx.connection.register_connection_opened_cb(self.after_update)
        self.pyvlx.connection.register_connection_closed_cb(self.after_update)
        self._disposed = False

    def dispose(self) -> None:
        """Unregister callbacks and clear local subscriptions."""
        if self._disposed:
            return
        self.pyvlx.connection.unregister_connection_opened_cb(self.after_update)
        self.pyvlx.connection.unregister_connection_closed_cb(self.after_update)
        self.device_updated_cbs.clear()
        self._disposed = True

    def register_device_updated_cb(self, device_updated_cb: CallbackType) -> None:
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb: CallbackType) -> None:
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def after_update(self) -> None:
        """Execute callbacks after internal state has been changed."""
        for device_updated_cb in self.device_updated_cbs:
            await device_updated_cb(self)

    def represents_same_node(self, other: Any) -> bool:
        """Return True if both objects represent the same physical node.

        Matching requires the same concrete node class. Identity is then resolved
        by serial number when both nodes have one. If exactly one node has a
        serial number, they are considered different. If both serial numbers are
        missing, node_id is used as fallback.

        This intentionally differs from __eq__, which compares full object state.
        Identity matching is used to decide whether two node instances can be
        treated as the same device (registered in the gateway) across reloads,
        even when runtime state (positions, frame history, callbacks) differs.
        """
        if not isinstance(other, Node):
            return False
        if type(self) is not type(other):
            return False
        if self.serial_number and other.serial_number:
            return self.serial_number == other.serial_number
        if self.serial_number or other.serial_number:
            return False
        return self.node_id == other.node_id

    async def rename(self, name: str) -> None:
        """Change name of node."""
        set_node_name = SetNodeName(pyvlx=self.pyvlx, node_id=self.node_id, name=name)
        await set_node_name.do_api_call()
        if not set_node_name.success:
            raise PyVLXException("Unable to rename node")
        self.name = name

    async def wink(self, wink_time: WinkTime = WinkTime.BY_MANUFACTURER, wait_for_completion: bool = True) -> None:
        """Identify node by making it wink."""
        wink_send = WinkSend(
            pyvlx=self.pyvlx,
            node_id=self.node_id,
            wink_time=wink_time,
            wait_for_completion=wait_for_completion,
        )
        await wink_send.send()

    @property
    def is_available(self) -> bool:
        """Return True if node is available."""
        return self.pyvlx.get_connected()

    def __str__(self) -> str:
        """Return object as readable string."""
        return (
            f'<{type(self).__name__} name="{self.name}" '
            f'node_id="{self.node_id}" '
            f'serial_number="{self.serial_number}" '
            f'last_frame_state="{self.last_frame_state}" '
            f'last_frame_status_reply="{self.last_frame_status_reply}"/>'
        )

    def __eq__(self, other: Any) -> bool:
        """Equal operator."""
        return (
            type(self).__name__ == type(other).__name__
            and self.__dict__ == other.__dict__
        )
