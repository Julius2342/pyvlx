
class PyVLXException(Exception):
    """Exception class for PyVLX library."""

    def __init__(self, message):
        """Initialize exception with the given error message."""
        super(PyVLXException, self).__init__(message)
