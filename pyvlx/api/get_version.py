"""Module for retrieving firmware version from API."""
from .api_event import ApiEvent
from .frames import FrameGetVersionConfirmation, FrameGetVersionRequest


class DtoVersion:
    """Object for KLF200 Data"""

    def __init__(self,
                 softwareversion=None, hardwareversion=None, productgroup=None, producttype=None):
        """Initialize DtoVersion class."""
        self.softwareversion = softwareversion
        self.hardwareversion = hardwareversion
        self.productgroup = productgroup
        self.producttype = producttype

    def __str__(self):
        """Return human readable string."""
        return (
            '<{} softwareversion="{}" hardwareversion="{}" '
            'productgroup="{}" producttype="{}"/>'.format(
                type(self).__name__,
                self.softwareversion, self.hardwareversion, self.productgroup, self.producttype
            )
        )


class GetVersion(ApiEvent):
    """Class for retrieving firmware version from API."""

    def __init__(self, pyvlx):
        """Initialize GetVersion class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.version = DtoVersion()

    async def handle_frame(self, frame):
        """Handle incoming API frame, return True if this was the expected frame."""
        if not isinstance(frame, FrameGetVersionConfirmation):
            return False
        self.version = DtoVersion(frame.software_version, frame.hardware_version,
                                  frame.product_group, frame.product_type)
        self.success = True
        return True

    def request_frame(self):
        """Construct initiating frame."""
        return FrameGetVersionRequest()
