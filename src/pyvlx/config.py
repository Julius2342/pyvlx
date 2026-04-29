"""Module for configuration."""
from typing import TYPE_CHECKING, Any, cast

import yaml

from .exception import PyVLXException
from .log import PYVLXLOG

if TYPE_CHECKING:
    from pyvlx import PyVLX


class Config:
    """Object for configuration."""

    DEFAULT_PORT = 51200

    def __init__(self,
                 pyvlx: "PyVLX",
                 path: str | None = None,
                 host: str | None = None,
                 password: str | None = None,
                 port: int | None = None):
        """Initialize Config class."""
        self.pyvlx = pyvlx
        self.host = host
        self.password = password
        self.port = port or self.DEFAULT_PORT
        if path is not None:
            self.read_config(path)

    def read_config(self, path: str) -> None:
        """Read configuration file."""
        PYVLXLOG.info("Reading config file: %s", path)
        try:
            with open(path, "r", encoding="utf-8") as filehandle:
                doc = yaml.safe_load(filehandle)
                self.test_configuration(doc, path)
                self.host = cast(str, doc["config"]["host"])
                self.password = cast(str, doc["config"]["password"])
                if "port" in doc["config"]:
                    self.port = doc["config"]["port"]
        except FileNotFoundError as not_found:
            raise PyVLXException(f"file does not exist: {not_found}") from not_found

    @staticmethod
    def test_configuration(doc: Any, path: str) -> None:
        """Test if configuration file is sane."""
        if "config" not in doc:
            raise PyVLXException(f"no element config found in: {path}")
        if "host" not in doc["config"]:
            raise PyVLXException(f"no element host found in: {path}")
        if "password" not in doc["config"]:
            raise PyVLXException(f"no element password found in: {path}")
