from typing import TYPE_CHECKING, Iterator
from pyvlx.actutator import Actutator
from pyvlx.exception import PyVLXException
from .api import GetSystemTable

if TYPE_CHECKING:
    from pyvlx import PyVLX

class Actutators() :
    """Object for storing node objects."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize Nodes object."""
        self.pyvlx = pyvlx
        self._actutators = []

    def __iter__(self) -> Iterator[Actutator]:
        """Iterate."""
        yield from self._actuators

    def __len__(self) -> int:
        """Return number of nodes."""
        return len(self._actutators)

    async def load(self) -> None:
        """Load all nodes via API."""
        _actutators_req = GetSystemTable(pyvlx=self.pyvlx)
        await _actutators_req.do_api_call()
        if not _actutators_req.success:
            raise PyVLXException("Unable to retrieve SystemTable information")
        self._actutators = []
        for act in _actutators_req.actutators :
            self._actutators.append( act )
