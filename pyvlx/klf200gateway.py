"""Module for basic klf200 gateway functions."""

from .api import (
    FactoryDefault, GetLocalTime, GetNetworkSetup, GetProtocolVersion,
    GetState, GetVersion, LeaveLearnState, PasswordEnter, Reboot, SetUTC)
from .exception import PyVLXException


class Klf200Gateway:
    """Class for node abstraction."""

    def __init__(self, pyvlx):
        """Initialize Node object."""
        self.pyvlx = pyvlx
        self.state = None
        self.network_setup = None
        self.password = None
        self.time = None
        self.protocol_version = None
        self.version = None
        self.device_updated_cbs = []

    def register_device_updated_cb(self, device_updated_cb):
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb):
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def after_update(self):
        """Execute callbacks after internal state has been changed."""
        for device_updated_cb in self.device_updated_cbs:
            # pylint: disable=not-callable
            await device_updated_cb(self)

    async def get_state(self):
        """Retrieve state from API."""
        get_state = GetState(pyvlx=self.pyvlx)
        await get_state.do_api_call()
        if not get_state.success:
            raise PyVLXException("Unable to retrieve state")
        self.state = get_state.state
        return get_state.success

    async def get_network_setup(self):
        """Retrieve network setup from API."""
        get_network_setup = GetNetworkSetup(pyvlx=self.pyvlx)
        await get_network_setup.do_api_call()
        if not get_network_setup.success:
            raise PyVLXException("Unable to retrieve network setup")
        self.network_setup = get_network_setup.networksetup
        return get_network_setup.success

    async def get_version(self):
        """Retrieve version from API."""
        get_version = GetVersion(pyvlx=self.pyvlx)
        await get_version.do_api_call()
        if not get_version.success:
            raise PyVLXException("Unable to retrieve version")
        self.version = get_version.version
        return get_version.success

    async def get_protocol_version(self):
        """Retrieve protocol version from API."""
        get_protocol_version = GetProtocolVersion(pyvlx=self.pyvlx)
        await get_protocol_version.do_api_call()
        if not get_protocol_version.success:
            raise PyVLXException("Unable to retrieve protocol version")
        self.protocol_version = get_protocol_version.protocolversion
        return get_protocol_version.success

    async def leave_learn_state(self):
        """Leave Learn state from API."""
        leave_learn_state = LeaveLearnState(pyvlx=self.pyvlx)
        await leave_learn_state.do_api_call()
        if not leave_learn_state.success:
            raise PyVLXException("Unable to leave learn state")
        return leave_learn_state.success

    async def set_utc(self):
        """Set UTC Clock."""
        setutc = SetUTC(pyvlx=self.pyvlx)
        await setutc.do_api_call()
        if not setutc.success:
            raise PyVLXException("Unable to set utc.")
        return setutc.success

    async def set_rtc_time_zone(self):  # pylint: disable=no-self-use
        """Set the RTC Time Zone."""
        # idontwant = setrtctimezone(pyvlx=self.pyvlx)
        raise PyVLXException("KLF 200 RTC Timezone Set not implemented")
        # return setrtctimezone.success

    async def reboot(self):
        """Reboot gateway."""
        reboot = Reboot(pyvlx=self.pyvlx)
        await reboot.do_api_call()
        if not reboot.success:
            raise PyVLXException("Unable to reboot gateway.")
        return reboot.success

    async def set_factory_default(self):
        """Set Gateway to Factory Default."""
        factorydefault = FactoryDefault(pyvlx=self.pyvlx)
        await factorydefault.do_api_call()
        if not factorydefault.success:
            raise PyVLXException("Unable to factory Default Reset gateway.")
        return factorydefault.success

    async def get_local_time(self):
        """Get local time from gateway."""
        getlocaltime = GetLocalTime(pyvlx=self.pyvlx)
        await getlocaltime.do_api_call()
        if not getlocaltime.success:
            raise PyVLXException("Unable to get local time.")
        self.time = getlocaltime.localtime
        return getlocaltime.success

    async def password_enter(self, password):
        """Get enter Password for gateway."""
        self.password = password
        passwordenter = PasswordEnter(pyvlx=self.pyvlx, password=self.password)
        await passwordenter.do_api_call()
        if not passwordenter.success:
            raise PyVLXException("Login to KLF 200 failed, check credentials")
        return passwordenter.success

    def __str__(self):
        """Return object as readable string."""
        return '<{} state="{}" network_setup="{}"  version="{}"  protocol_version="{}"/>'.format(
            type(self).__name__,
            str(self.state),
            str(self.network_setup),
            str(self.version),
            str(self.protocol_version),
        )
