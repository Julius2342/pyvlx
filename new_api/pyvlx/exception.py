"""Module for PyVLX Exceptions."""


class PyVLXException(Exception):
    """Default PyVLX Exception."""

    def __init__(self, description, **kwargs):
        """Initialize PyVLXException class."""
        super().__init__(description)
        self.description = description
        self.parameter = kwargs

    def _format_parameter(self):
        return " ".join(['%s="%s"' % (key, value) for (key, value) in sorted(self.parameter.items())])

    def __str__(self):
        """Return object as readable string."""
        return '<PyVLXException description="{0}" {1}/>' \
            .format(self.description, self._format_parameter())
