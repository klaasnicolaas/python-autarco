"""Asynchronous Python client for Autarco API."""
from __future__ import annotations

import asyncio
import socket
from dataclasses import dataclass
from importlib import metadata
from typing import Any, Self, cast

from aiohttp import BasicAuth, ClientError, ClientResponseError, ClientSession
from aiohttp.hdrs import METH_GET
from yarl import URL

from .exceptions import (
    AutarcoAuthenticationError,
    AutarcoConnectionError,
    AutarcoError,
)
from .models import Account, Inverter, Solar

VERSION = metadata.version(__package__)


@dataclass
class Autarco:
    """Main class for handling connections to Autarco."""

    email: str
    password: str

    request_timeout: float = 10.0
    session: ClientSession | None = None

    _close_session: bool = False

    async def _request(
        self,
        uri: str,
        *,
        method: str = METH_GET,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Handle a request to the Autarco API.

        A generic method for sending/handling HTTP requests done against
        the Autarco API.

        Args:
        ----
            uri: Request URI, without '/', for example, 'status'.
            method: HTTP method to use.
            data: Dictionary of data send to the Autarco API.

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
                    json=data,
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
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected response from the Autarco API"
            raise AutarcoError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        return cast(dict[str, Any], await response.json())

    async def get_public_key(self) -> str:
        """Get the public key.

        Returns
        -------
            The public key as string.

        """
        data = await self._request("")
        key: str = data[0]["public_key"]
        return key

    async def inverters(self, public_key: str) -> list[Inverter]:
        """Get a list of all used inverters.

        Args:
        ----
            public_key: The public key from your account.

        Returns:
        -------
            A list of Inverter objects.

        """
        results: dict[str, Any] = {}

        data = await self._request(f"{public_key}/power")
        for number, item in enumerate(data["inverters"].items(), 1):
            inverter = Inverter.from_json(item)
            results[f"Inverter {number}"] = inverter
        return results

    async def solar(self, public_key: str) -> Solar:
        """Get information about the solar production.

        Args:
        ----
            public_key: The public key from your account.

        Returns:
        -------
            An Solar object.

        """
        data = await self._request(f"{public_key}/")
        return Solar.from_json(data)

    async def account(self, public_key: str) -> Account:
        """Get information about your account.

        Args:
        ----
            public_key: The public key from your account.

        Returns:
        -------
            An Account object.

        """
        data = await self._request(f"{public_key}/")
        return Account.from_json(data)

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
