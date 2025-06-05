from typing import TYPE_CHECKING, Iterator
from .api import GetSystemTable
from pyvlx.actutator import Actutator

if TYPE_CHECKING:
    from pyvlx import PyVLX

class Actutators() :
  """Object for storing node objects."""

  def __init__(self, pyvlx: "PyVLX"):
    """Initialize Nodes object."""
    self.pyvlx = pyvlx
    self._actuators: List[ Actutator ] = []

  def __iter__(self) -> Iterator[Actutator]:
    """Iterate."""
    yield from self._actuators

  def __len__(self) -> int:
    """Return number of nodes."""
    return len(self._actutators)

  def clear(self) -> None:
    """Clear internal node array."""
    self._actutators = []

  async def load(self) -> None:
    """Load all nodes via API."""
    _actutatorsReq = GetSystemTable(pyvlx=self.pyvlx)
    await _actutatorsReq.do_api_call()
    if not _actutatorsReq.success:
      raise PyVLXException("Unable to retrieve SystemTable information")
    self.clear()
    for act in _actutatorsReq :
      self._actuators.append( act );
