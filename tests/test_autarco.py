"""Basic tests for the Autarco API."""

# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import pytest
from aiohttp import ClientError, ClientResponse, ClientSession
from aresponses import Response, ResponsesMockServer

from autarco import Autarco
from autarco.exceptions import (
    AutarcoConnectionError,
    AutarcoError,
)

from . import load_fixtures


async def test_json_request(
    aresponses: ResponsesMockServer,
    autarco_client: Autarco,
) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("account.json"),
        ),
    )
    response = await autarco_client._request("test")
    assert response is not None
    await autarco_client.close()


async def test_internal_session(aresponses: ResponsesMockServer) -> None:
    """Test JSON response is handled correctly."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("account.json"),
        ),
    )
    async with Autarco(email="test@autarco.com", password="energy") as client:
        await client._request("test")


async def test_timeout(aresponses: ResponsesMockServer) -> None:
    """Test request timeout from Autarco API."""

    # Faking a timeout by sleeping
    async def response_handler(_: ClientResponse) -> Response:
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!",
        )

    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        response_handler,
    )

    async with ClientSession() as session:
        client = Autarco(
            email="test@autarco.com",
            password="energy",
            session=session,
            request_timeout=0.1,
        )
        with pytest.raises(AutarcoConnectionError):
            assert await client._request("test")


async def test_content_type(
    aresponses: ResponsesMockServer,
    autarco_client: Autarco,
) -> None:
    """Test request content type error from Autarco API."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "blabla/blabla"},
        ),
    )
    with pytest.raises(AutarcoError):
        assert await autarco_client._request("test")


async def test_client_error() -> None:
    """Test request client error from Autarco API."""
    async with ClientSession() as session:
        client = Autarco(email="test@autarco.com", password="energy", session=session)
        with (
            patch.object(
                session,
                "request",
                side_effect=ClientError,
            ),
            pytest.raises(AutarcoConnectionError),
        ):
            assert await client._request("test")


async def test_response_status_404(
    aresponses: ResponsesMockServer,
    autarco_client: Autarco,
) -> None:
    """Test HTTP 404 response handling."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(text="GIVE ME SOLARPOWER!", status=404),
    )
    with pytest.raises(AutarcoConnectionError):
        assert await autarco_client._request("test")
