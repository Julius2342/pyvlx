"""Module for configuration."""
import yaml

from .exception import PyVLXException
from .log import PYVLXLOG


class Config:
    """Object for configuration."""

    DEFAULT_PORT = 51200

    def __init__(self, pyvlx, path=None, host=None, password=None, port=None):
        """Initialize Config class."""
        self.pyvlx = pyvlx
        self.host = host
        self.password = password
        self.port = port or self.DEFAULT_PORT
        if path is not None:
            self.read_config(path)

    def read_config(self, path):
        """Read configuration file."""
        PYVLXLOG.info('Reading config file: %s', path)
        try:
            with open(path, 'r') as filehandle:
                doc = yaml.safe_load(filehandle)
                self.test_configuration(doc, path)
                self.host = doc['config']['host']
                self.password = doc['config']['password']
                if 'port' in doc['config']:
                    self.port = doc['config']['port']
        except FileNotFoundError as ex:
            raise PyVLXException('file does not exist: {0}'.format(ex))

    @staticmethod
    def test_configuration(doc, path):
        """Test if configuration file is sane."""
        if 'config' not in doc:
            raise PyVLXException('no element config found in: {0}'.format(path))
        if 'host' not in doc['config']:
            raise PyVLXException('no element host found in: {0}'.format(path))
        if 'password' not in doc['config']:
            raise PyVLXException('no element password found in: {0}'.format(path))
