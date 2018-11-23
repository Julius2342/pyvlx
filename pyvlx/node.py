"""
Module for basic object for nodes.

Node object is an interface class and should
be derived by other objects like window openers
and roller shutters.
"""


# pylint: disable=too-few-public-methods
class Node:
    """Class for node abstraction."""

    def __init__(self, pyvlx, node_id, name):
        """Initialize Node object."""
        self.pyvlx = pyvlx
        self.node_id = node_id
        self.name = name

    def __eq__(self, other):
        """Equal operator."""
        return self.__dict__ == other.__dict__
