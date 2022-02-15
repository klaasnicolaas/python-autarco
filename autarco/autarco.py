"""Asynchronous Python client for Autarco API."""
from __future__ import annotations

import asyncio
import socket
from collections.abc import Mapping
from dataclasses import dataclass
from importlib import metadata
from typing import Any

import aiohttp
import async_timeout
from aiohttp.client import ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import (
    AutarcoAuthenticationError,
    AutarcoConnectionError,
    AutarcoConnectionTimeoutError,
    AutarcoError,
)
from .models import Account, Inverter, Solar


@dataclass
class Autarco:
    """Main class for handling connections to Autarco."""

    public_key: str
    username: str
    password: str

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        params: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """Handle a request to the Autarco API.

        A generic method for sending/handling HTTP requests done against
        the Autarco API.

        Args:
            uri: Request URI, without '/', for example, 'status'.
            method: HTTP method to use.
            params: Dictionary of parameters to send to the Autarco API.

        Returns:
            The response data from the Autarco API.

        Raises:
            AutarcoAuthenticationError: If the username or password is invalid.
            AutarcoConnectionError: An error occurred while communicating
                with the Autarco API.
            AutarcoConnectionTimeoutError: A timeout occurred while communicating
                with the Autarco API.
            AutarcoError: Received an unexpected response from the
                Autarco API.
        """
        version = metadata.version(__package__)
        url = URL.build(scheme="https", host="my.autarco.com", path="/api/site/").join(
            URL(uri)
        )

        headers = {
            "Accept": "application/json",
            "User-Agent": f"PythonAutarco/{version}",
        }

        if self.session is None:
            self.session = ClientSession()
            self._close_session = True

        # Set basic auth credentials.
        auth = aiohttp.BasicAuth(self.username, self.password)

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.request(
                    method,
                    url,
                    auth=auth,
                    headers=headers,
                    params=params,
                    ssl=True,
                )
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            raise AutarcoConnectionTimeoutError(
                "Timeout occurred while connecting to Autarco API"
            ) from exception
        except ClientResponseError as exception:
            if exception.status == 401:
                raise AutarcoAuthenticationError(
                    "Authentication to the Autarco API failed"
                ) from exception
            raise AutarcoConnectionError(
                "Error occurred while connecting to the Autarco API"
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            raise AutarcoConnectionError(
                "Error occurred while communicating with the Autarco API"
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            raise AutarcoError(
                "Unexpected response from the Autarco API",
                {"Content-Type": content_type, "response": text},
            )

        return await response.json()

    async def all_inverters(self) -> Inverter:
        """Get a list of all used inverters.

        Returns:
            A list of Inverter objects.
        """
        results = []

        data = await self._request(f"{self.public_key}/power")
        for item in data["inverters"].items():
            results.append(Inverter.from_json(item))
        return results

    async def solar(self) -> Solar:
        """Get.

        Returns:
            An Solar object.
        """

        data = await self._request(f"{self.public_key}/")
        return Solar.from_json(data)

    async def account(self) -> Account:
        """Get.

        Returns:
            An Account object.
        """

        data = await self._request(f"{self.public_key}/")
        return Account.from_json(data)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Autarco:
        """Async enter.

        Returns:
            The Autarco object.
        """
        return self

    async def __aexit__(self, *_exc_info) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
