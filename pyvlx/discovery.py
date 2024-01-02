"""Module to discover Velux KLF200 devices on the network."""
import asyncio
from asyncio import AbstractEventLoop
from dataclasses import dataclass

from zeroconf import (
    IPVersion, ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf)
from zeroconf.asyncio import AsyncZeroconf

HOST_STARTS_WITH: str = "VELUX_KLF_LAN"
SERVICE_TYPE: str = "_http._tcp.local."


@dataclass
class VeluxHost():
    """Class to store Velux KLF200 host information."""
    
    hostname: str
    ip_address: str


class VeluxDiscovery():
    """Class to discover Velux KLF200 devices on the network."""

    def __init__(
            self,
            loop: AbstractEventLoop,
            zeroconf: AsyncZeroconf = AsyncZeroconf(),
            listening_time_in_seconds: float = 10
    ) -> None:
        """Initialize VeluxDiscovery object."""
        self.zc: AsyncZeroconf = zeroconf
        self.loop: AbstractEventLoop = loop
        self.listening_time_in_seconds: float = listening_time_in_seconds
        self.hosts: list[VeluxHost | None] = []
        self.infos: list[ServiceInfo | None] = []

    async def _set_hosts(self) -> None:
        """Set hosts from zeroconf ServiceInfo."""
        for info in self.infos:
            if info:
                host = VeluxHost(
                    hostname=info.name.replace("._http._tcp.local.", ""),
                    ip_address=info.parsed_addresses(version=IPVersion.V4Only)[0]
                )
                self.hosts.append(host)

    async def _listen_for_services(self) -> None:
        """Listen for zeroconf ServiceInfo."""
        self.hosts.clear()
        waited_time: float = 0
        sleep_time: float = 0.5
        names: list = []
        zeroconf = self.zc.zeroconf

        def handler(zeroconf: Zeroconf, service_type: str, state_change: ServiceStateChange, name: str) -> None:  # pylint: disable=W0613:unused-argument
            if name not in names:
                names.append(name)

        browser: ServiceBrowser = ServiceBrowser(zeroconf, SERVICE_TYPE, handlers=[handler])

        while not self.hosts:
            await asyncio.sleep(sleep_time)
            waited_time += sleep_time
            if waited_time > self.listening_time_in_seconds:
                break
            for name in names:
                if name.startswith(HOST_STARTS_WITH):
                    self.infos.append(zeroconf.get_service_info(type_=SERVICE_TYPE, name=name))
            await self._set_hosts()
        browser.cancel()

    async def discover_hosts(self) -> list[VeluxHost | None]:
        """Discover Velux KLF200 devices from the network."""
        if not self.hosts:
            await self._listen_for_services()
        return self.hosts
