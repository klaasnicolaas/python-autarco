"""Asynchronous Python client for Autarco API."""

from __future__ import annotations

import asyncio
import json
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self

from aiohttp import BasicAuth, ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import (
    AutarcoAuthenticationError,
    AutarcoConnectionError,
    AutarcoError,
)
from .models import (
    AccountResponse,
    AccountSite,
    Battery,
    EnergyResponse,
    Inverter,
    PowerResponse,
    Site,
    Solar,
    Stats,
)

VERSION = metadata.version(__package__)


@dataclass
class Autarco:
    """Main class for handling connections to Autarco."""

    email: str
    password: str

    request_timeout: float = 15.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: dict[str, Any] | None = None,
    ) -> str:
        """Handle a request to the Autarco API.

        A generic method for sending/handling HTTP requests done against
        the Autarco API.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'.
            method: HTTP method to use.
            params: Query parameters to send with the request.

        Returns:
        -------
            The response data from the Autarco API.

        Raises:
        ------
            AutarcoAuthenticationError: If the email or password is invalid.
            AutarcoConnectionError: An error occurred while communicating
                with the Autarco API.
            AutarcoConnectionTimeoutError: A timeout occurred while communicating
                with the Autarco API.
            AutarcoError: Received an unexpected response from the
                Autarco API.

        """
        url = URL.build(
            scheme="https",
            host="my.autarco.com",
            path="/api/site/",
        ).join(URL(uri))

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonAutarco/{VERSION}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        # Set basic auth credentials.
        auth = BasicAuth(self.email, self.password)

        try:
            async with asyncio.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    auth=auth,
                    headers=headers,
                    params=params,
                    ssl=True,
                )
                response.raise_for_status()
        except TimeoutError as exception:
            msg = "Timeout occurred while connecting to Autarco API"
            raise AutarcoConnectionError(msg) from exception
        except ClientResponseError as exception:
            if exception.status == 401:
                msg = "Authentication to the Autarco API failed"
                raise AutarcoAuthenticationError(msg) from exception
            msg = "Error occurred while communicating with the Autarco API"
            raise AutarcoConnectionError(msg) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with the Autarco API"
            raise AutarcoConnectionError(msg) from exception

        content_type = response.headers.get("Content-Type", "")
        text = await response.text()
        if "application/json" not in content_type:
            msg = "Unexpected response from the Autarco API"
            raise AutarcoError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return text

    async def _get_combined_data(self, public_key: str) -> dict[str, Any]:
        """Get a combined dictionary with power and energy data from a site.

        Args:
        ----
            public_key: The public key from your site.

        Returns:
        -------
            A dictionary with combined power and energy data.

        """
        power_response = await self._request(f"{public_key}/kpis/power")
        energy_response = await self._request(f"{public_key}/kpis/energy")
        return {**json.loads(power_response), **json.loads(energy_response)}

    async def get_account(self) -> list[AccountSite]:
        """Get account with list of sites.

        Returns
        -------
            A list of Site objects.

        """
        response = await self._request("")
        return AccountResponse.from_json(response).sites

    async def get_inverters(self, public_key: str) -> dict[str, Inverter]:
        """Get a list of all used inverters.

        Args:
        ----
            public_key: The public key from the specific site.

        Returns:
        -------
            A list of Inverter objects.

        """
        response = await self._request(f"{public_key}/power")
        return PowerResponse.from_json(response).inverters

    async def get_power_statistics(
        self, public_key: str, query_range: str = "day"
    ) -> Stats:
        """Get the statistics of the inverters.

        Args:
        ----
            public_key: The public key from the specific site.
            query_range: The range of time to get the statistics for.

        Returns:
        -------
            A list of Inverter objects.

        """
        response = await self._request(f"{public_key}/power", params={"r": query_range})
        return PowerResponse.from_json(response).stats

    async def get_energy_statistics(
        self, public_key: str, query_range: str = "month"
    ) -> Stats:
        """Get the statistics of the inverters.

        Args:
        ----
            public_key: The public key from the specific site.
            query_range: The range of time to get the statistics for.

        Returns:
        -------
            A list of Inverter objects.

        """
        response = await self._request(
            f"{public_key}/energy", params={"r": query_range}
        )
        return EnergyResponse.from_json(response).stats

    async def get_solar(self, public_key: str) -> Solar:
        """Get information about the solar production from a site.

        Args:
        ----
            public_key: The public key from your site.

        Returns:
        -------
            An Solar object.

        """
        combined_data = await self._get_combined_data(public_key)
        return Solar.from_dict(combined_data)

    async def get_site(self, public_key: str) -> Site:
        """Get information about your system site.

        Args:
        ----
            public_key: The public key from your site.

        Returns:
        -------
            An Site object.

        """
        response = await self._request(f"{public_key}/")
        return Site.from_json(response)

    async def get_battery(self, public_key: str) -> Battery:
        """Get information about the battery from a site.

        Args:
        ----
            public_key: The public key from your site.

        Returns:
        -------
            An Battery object.

        """
        combined_data = await self._get_combined_data(public_key)
        return Battery.from_dict(combined_data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The Autarco object.

        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.

        """
        await self.close()
