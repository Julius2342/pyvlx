"""Module for basic klf200 gateway functions."""

from typing import TYPE_CHECKING, Awaitable, Callable, List, Optional

from .api import (
    FactoryDefault, GetLocalTime, GetNetworkSetup, GetProtocolVersion,
    GetState, GetVersion, HouseStatusMonitorDisable, HouseStatusMonitorEnable,
    LeaveLearnState, PasswordEnter, Reboot, SetUTC)
from .dataobjects import (
    DtoLocalTime, DtoNetworkSetup, DtoProtocolVersion, DtoState, DtoVersion)
from .exception import PyVLXException

if TYPE_CHECKING:
    from pyvlx import PyVLX

CallbackType = Callable[["Klf200Gateway"], Awaitable[None]]


class Klf200Gateway:
    """Class for node abstraction."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize Node object."""
        self.pyvlx = pyvlx
        self.state: Optional[DtoState] = None
        self.network_setup: Optional[DtoNetworkSetup] = None
        self.password: Optional[str] = None
        self.time: Optional[DtoLocalTime] = None
        self.protocol_version: Optional[DtoProtocolVersion] = None
        self.version: Optional[DtoVersion] = None
        self.device_updated_cbs: List[CallbackType] = []
        self.house_status_monitor_enabled = False

    def register_device_updated_cb(self, device_updated_cb: CallbackType) -> None:
        """Register device updated callback."""
        self.device_updated_cbs.append(device_updated_cb)

    def unregister_device_updated_cb(self, device_updated_cb: CallbackType) -> None:
        """Unregister device updated callback."""
        self.device_updated_cbs.remove(device_updated_cb)

    async def after_update(self) -> None:
        """Execute callbacks after internal state has been changed."""
        for device_updated_cb in self.device_updated_cbs:
            # pylint: disable=not-callable
            await device_updated_cb(self)

    async def get_state(self) -> bool:
        """Retrieve state from API."""
        get_state = GetState(pyvlx=self.pyvlx)
        await get_state.do_api_call()
        if not get_state.success:
            raise PyVLXException("Unable to retrieve state")
        self.state = get_state.state
        return get_state.success

    async def get_network_setup(self) -> bool:
        """Retrieve network setup from API."""
        get_network_setup = GetNetworkSetup(pyvlx=self.pyvlx)
        await get_network_setup.do_api_call()
        if not get_network_setup.success:
            raise PyVLXException("Unable to retrieve network setup")
        self.network_setup = get_network_setup.networksetup
        return get_network_setup.success

    async def get_version(self) -> bool:
        """Retrieve version from API."""
        get_version = GetVersion(pyvlx=self.pyvlx)
        await get_version.do_api_call()
        if not get_version.success:
            raise PyVLXException("Unable to retrieve version")
        self.version = get_version.version
        return get_version.success

    async def get_protocol_version(self) -> bool:
        """Retrieve protocol version from API."""
        get_protocol_version = GetProtocolVersion(pyvlx=self.pyvlx)
        await get_protocol_version.do_api_call()
        if not get_protocol_version.success:
            raise PyVLXException("Unable to retrieve protocol version")
        self.protocol_version = get_protocol_version.protocolversion
        return get_protocol_version.success

    async def leave_learn_state(self) -> bool:
        """Leave Learn state from API."""
        leave_learn_state = LeaveLearnState(pyvlx=self.pyvlx)
        await leave_learn_state.do_api_call()
        if not leave_learn_state.success:
            raise PyVLXException("Unable to leave learn state")
        return leave_learn_state.success

    async def set_utc(self) -> bool:
        """Set UTC Clock."""
        setutc = SetUTC(pyvlx=self.pyvlx)
        await setutc.do_api_call()
        if not setutc.success:
            raise PyVLXException("Unable to set utc.")
        return setutc.success

    async def set_rtc_time_zone(self) -> None:
        """Set the RTC Time Zone."""
        # idontwant = setrtctimezone(pyvlx=self.pyvlx)
        raise PyVLXException("KLF 200 RTC Timezone Set not implemented")
        # return setrtctimezone.success

    async def reboot(self) -> bool:
        """Reboot gateway."""
        reboot = Reboot(pyvlx=self.pyvlx)
        await reboot.do_api_call()
        if not reboot.success:
            raise PyVLXException("Unable to reboot gateway.")
        return reboot.success

    async def set_factory_default(self) -> bool:
        """Set Gateway to Factory Default."""
        factorydefault = FactoryDefault(pyvlx=self.pyvlx)
        await factorydefault.do_api_call()
        if not factorydefault.success:
            raise PyVLXException("Unable to factory Default Reset gateway.")
        return factorydefault.success

    async def get_local_time(self) -> bool:
        """Get local time from gateway."""
        getlocaltime = GetLocalTime(pyvlx=self.pyvlx)
        await getlocaltime.do_api_call()
        if not getlocaltime.success:
            raise PyVLXException("Unable to get local time.")
        self.time = getlocaltime.localtime
        return getlocaltime.success

    async def password_enter(self, password: str) -> bool:
        """Get enter Password for gateway."""
        self.password = password
        passwordenter = PasswordEnter(pyvlx=self.pyvlx, password=self.password)
        await passwordenter.do_api_call()
        if not passwordenter.success:
            raise PyVLXException("Login to KLF 200 failed, check credentials")
        return passwordenter.success

    async def house_status_monitor_enable(self, pyvlx: "PyVLX") -> None:
        """Enable house status monitor."""
        status_monitor_enable = HouseStatusMonitorEnable(pyvlx=pyvlx)
        await status_monitor_enable.do_api_call()
        if not status_monitor_enable.success:
            raise PyVLXException("Unable enable house status monitor.")
        self.house_status_monitor_enabled = True

    async def house_status_monitor_disable(self, pyvlx: "PyVLX", timeout: Optional[int] = None) -> None:
        """Disable house status monitor."""
        status_monitor_disable = HouseStatusMonitorDisable(pyvlx=pyvlx)
        if timeout is not None:
            status_monitor_disable.timeout_in_seconds = timeout
        await status_monitor_disable.do_api_call()
        if not status_monitor_disable.success:
            raise PyVLXException("Unable disable house status monitor.")
        self.house_status_monitor_enabled = False

    def __str__(self) -> str:
        """Return object as readable string."""
        return '<{} state="{}" network_setup="{}"  version="{}"  protocol_version="{}"/>'.format(
            type(self).__name__,
            str(self.state),
            str(self.network_setup),
            str(self.version),
            str(self.protocol_version),
        )
