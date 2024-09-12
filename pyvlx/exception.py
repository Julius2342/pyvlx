"""Module for PyVLX Exceptions."""
from typing import Any


class PyVLXException(Exception):
    """Default PyVLX Exception."""

    def __init__(self, description: str, **kwargs: Any):
        """Initialize PyVLXException class."""
        super().__init__(description)
        self.description = description
        self.parameter = kwargs

    def _format_parameter(self) -> str:
        return " ".join(
            [
                '%s="%s"' % (key, value)
                for (key, value) in sorted(self.parameter.items())
            ]
        )

    def __str__(self) -> str:
        """Return object as readable string."""
        return '<{} description="{}" {}/>'.format(
            type(self).__name__, self.description, self._format_parameter()
        )
