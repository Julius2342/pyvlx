"""Module to discover Velux KLF200 devices on the network."""
import asyncio
from asyncio import Event, Future, Task
from dataclasses import dataclass
from typing import Any, Optional

from zeroconf import IPVersion
from zeroconf.asyncio import (
    AsyncServiceBrowser, AsyncServiceInfo, AsyncZeroconf)

SERVICE_STARTS_WITH: str = "VELUX_KLF_LAN"
SERVICE_TYPE: str = "_http._tcp.local."


@dataclass
class VeluxHost():
    """Class to store Velux KLF200 host information."""

    hostname: str
    ip_address: str


class VeluxDiscovery():
    """Class to discover Velux KLF200 devices on the network."""

    hosts: list[VeluxHost | None] = []
    infos: list[AsyncServiceInfo | None] = []

    def __init__(self, zeroconf: AsyncZeroconf,) -> None:
        """Initialize VeluxDiscovery object."""
        self.zc: AsyncZeroconf = zeroconf

    async def _async_discover_hosts(self, min_wait_time: float, expected_hosts: int | None) -> None:
        """Listen for zeroconf ServiceInfo."""
        self.hosts.clear()
        service_names: list[str] = []
        tasks: list[Task] = []
        got_host: Event = Event()

        def add_info_and_host(fut: Future) -> None:
            info: AsyncServiceInfo = fut.result()
            self.infos.append(info)
            host = VeluxHost(
                hostname=info.name.replace("._http._tcp.local.", ""),
                ip_address=info.parsed_addresses(version=IPVersion.V4Only)[0],
            )
            self.hosts.append(host)
            got_host.set()

        def handler(name: str, **kwargs: Any) -> None:  # pylint: disable=W0613:unused-argument
            if name.startswith(SERVICE_STARTS_WITH):
                if name not in service_names:
                    service_names.append(name)
                    task = asyncio.create_task(self.zc.async_get_service_info(type_=SERVICE_TYPE, name=name))
                    task.add_done_callback(add_info_and_host)
                    tasks.append(task)

        browser: AsyncServiceBrowser = AsyncServiceBrowser(self.zc.zeroconf, SERVICE_TYPE, handlers=[handler])
        if expected_hosts:
            while len(self.hosts) < expected_hosts:
                await got_host.wait()
                got_host.clear()
        while not self.hosts:
            await asyncio.sleep(min_wait_time)
        await browser.async_cancel()
        await asyncio.gather(*tasks)

    async def async_discover_hosts(
        self,
        timeout: float = 10,
        min_wait_time: float = 3,
        expected_hosts: Optional[int] = None
    ) -> bool:
        """Return true if Velux KLF200 devices found on the network.

        This function creates a zeroconf AsyncServiceBrowser and
        waits min_wait_time (seconds) for ServiceInfos from hosts.
        Some devices may take some time to respond (i.e. if they currently have a high CPU load).
        If one or more Hosts are found, the function cancels the ServiceBrowser and returns true.
        If expected_hosts is set, the function ignores min_wait_time and returns true once expected_hosts are found.
        If timeout (seconds) is exceeded, the function returns false.
        """
        try:
            async with asyncio.timeout(timeout):
                await self._async_discover_hosts(min_wait_time, expected_hosts)
        except TimeoutError:
            return False
        return True
