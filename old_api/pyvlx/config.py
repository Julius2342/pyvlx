"""Module for configuration."""

import yaml

from .exception import PyVLXException


# pylint: disable=too-few-public-methods
class Config:
    """Object for configuration."""

    def __init__(self, pyvlx, path=None, host=None, password=None):
        """Initialize Config class."""
        self.pyvlx = pyvlx
        if path is not None:
            self.read_config(path)
        if host is not None:
            self.host = host
        if password is not None:
            self.password = password

    def read_config(self, path):
        """Read configuration file."""
        self.pyvlx.logger.info('Reading config file: ', path)
        try:
            with open(path, 'r') as filehandle:
                doc = yaml.load(filehandle)
                if 'config' not in doc:
                    raise PyVLXException('no element config found in: {0}'.format(path))
                if 'host' not in doc['config']:
                    raise PyVLXException('no element host found in: {0}'.format(path))
                if 'password' not in doc['config']:
                    raise PyVLXException('no element password found in: {0}'.format(path))
                self.host = doc['config']['host']
                self.password = doc['config']['password']
        except FileNotFoundError as ex:
            raise PyVLXException('file does not exist: {0}'.format(ex))
