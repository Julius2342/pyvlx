"""Actuators."""
from typing import TYPE_CHECKING, Iterator

from pyvlx.actuator import Actuator
from pyvlx.exception import PyVLXException

from .api import GetSystemTable

if TYPE_CHECKING:
    from pyvlx import PyVLX


class Actuators() :
    """Object for storing node objects."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize Nodes object."""
        self.pyvlx = pyvlx
        self._actuators : list[Actuator] = []

    def __iter__(self) -> Iterator[Actuator]:
        """Iterate."""
        yield from self._actuators

    def __len__(self) -> int:
        """Return number of nodes."""
        return len(self._actuators)

    async def load(self) -> None:
        """Load all nodes via API."""
        _actuators_req = GetSystemTable(pyvlx=self.pyvlx)
        await _actuators_req.do_api_call()
        if not _actuators_req.success:
            raise PyVLXException("Unable to retrieve SystemTable information")
        self._actuators = []
        for act in _actuators_req.actuators :
            self._actuators.append(act)
