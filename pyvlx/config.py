"""Module for configuration."""


class Config:
    """Class for Configuration."""

    # pylint: disable=too-few-public-methods

    def __init__(self, host, password, port=51200):
        """Initialize configuration."""
        self.port = port
        self.host = host
        self.password = password
