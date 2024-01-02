"""Module to discover Velux KLF200 devices on the network."""
import asyncio
from asyncio import AbstractEventLoop, Future
from dataclasses import dataclass
from typing import Any

from zeroconf import IPVersion
from zeroconf.asyncio import (
    AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf)

from .log import PYVLXLOG

SERVICE_STARTS_WITH: str = "VELUX_KLF_LAN"
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
            zeroconf: AsyncZeroconf,
    ) -> None:
        """Initialize VeluxDiscovery object."""
        self.zc: AsyncZeroconf = zeroconf
        self.loop: AbstractEventLoop = loop
        self.hosts: list[VeluxHost | None] = []
        self.infos: list[AsyncServiceInfo | None] = []

    async def _async_discover_hosts(self, min_wait_time: float) -> None:
        """Listen for zeroconf ServiceInfo."""
        self.hosts.clear()
        service_names: list[str] = []

        def handler(name: str, **kwargs: Any) -> None:  # pylint: disable=W0613:unused-argument
            if name.startswith(SERVICE_STARTS_WITH):
                if name not in service_names:
                    service_names.append(name)

        def add_info_and_host(fut: Future) -> None:
            info: AsyncServiceInfo = fut.result()
            self.infos.append(info)
            host = VeluxHost(
                hostname=info.name.replace("._http._tcp.local.", ""),
                ip_address=info.parsed_addresses(version=IPVersion.V4Only)[0],
            )
            PYVLXLOG.debug("Found KLF200 in network: %s", host)
            self.hosts.append(host)

        browser: AsyncServiceBrowser = AsyncServiceBrowser(self.zc.zeroconf, SERVICE_TYPE, handlers=[handler])

        while not self.hosts:
            await asyncio.sleep(min_wait_time)
            async with asyncio.TaskGroup() as tg:
                for name in service_names:
                    task = tg.create_task(self.zc.async_get_service_info(type_=SERVICE_TYPE, name=name))
                    task.add_done_callback(add_info_and_host)
        await browser.async_cancel()

    async def async_discover_hosts(self, timeout: float = 10, min_wait_time: float = 1) -> bool:
        """Return true if Velux KLF200 devices found on the network.

        This function creates a zeroconf AsyncServiceBrowser and waits min_wait_time (seconds) for ServiceInfos from hosts.
        Some devices may take some time to respond (i.e. if they currently have a high CPU load).
        If one or more Hosts are found, the function cancels the ServiceBrowser and returns true.
        If no Host is found during timeout (seconds), false is returned.
        """
        try:
            async with asyncio.timeout(timeout):
                await self._async_discover_hosts(min_wait_time)
        except TimeoutError:
            return False
        return True
