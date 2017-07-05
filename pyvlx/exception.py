
class PyVLXException(Exception):
    """Exception class for PyVLX library."""

    def __init__(self, message):
        """Initialize exception with the given error message."""
        super(PyVLXException, self).__init__(message)



class InvalidToken(PyVLXException):
    """KLF 200 token invalid or expired."""

    def __init__(self, error_code):
        """Initialize exception with the given error message."""
        super(InvalidToken, self).__init__("Invalid Token")
        self.error_code = error_code
