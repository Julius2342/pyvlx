"""
Module for basic object for nodes.

Node object is an interface class and should
be derived by other objects like window openers
and roller shutters.
"""
from typing import TYPE_CHECKING, Any, Awaitable, Callable, List, Optional

from .api import SetNodeName
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
        self.device_updated_cbs: List[CallbackType] = []

    def register_device_updated_cb(self, device_updated_cb: CallbackType) -> None:
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb: CallbackType) -> None:
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def after_update(self) -> None:
        """Execute callbacks after internal state has been changed."""
        for device_updated_cb in self.device_updated_cbs:
            # pylint: disable=not-callable
            self.pyvlx.loop.create_task(device_updated_cb(self))  # type: ignore

    async def rename(self, name: str) -> None:
        """Change name of node."""
        set_node_name = SetNodeName(pyvlx=self.pyvlx, node_id=self.node_id, name=name)
        await set_node_name.do_api_call()
        if not set_node_name.success:
            raise PyVLXException("Unable to rename node")
        self.name = name

    def __str__(self) -> str:
        """Return object as readable string."""
        return (
            '<{} name="{}" '
            'node_id="{}" '
            'serial_number="{}"/>'.format(
                type(self).__name__, self.name, self.node_id, self.serial_number
            )
        )

    def __eq__(self, other: Any) -> bool:
        """Equal operator."""
        return (
            type(self).__name__ == type(other).__name__
            and self.__dict__ == other.__dict__
        )
