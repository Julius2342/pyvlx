"""Module for exceptions."""


class PyVLXException(Exception):
    """Exception class for PyVLX library."""

    def __init__(self, description):
        """Initialize exception with the given error message."""
        super(PyVLXException, self).__init__()
        self.description = description

    def __str__(self):
        """Return object as readable string."""
        return '<PyVLXException description="{0}" />' \
            .format(self.description)


class InvalidToken(PyVLXException):
    """KLF 200 token invalid or expired."""

    def __init__(self, error_code):
        """Initialize exception with the given error message."""
        super(InvalidToken, self).__init__("Invalid Token")
        self.error_code = error_code
