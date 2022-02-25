"""Basic tests for the Autarco API."""
# pylint: disable=protected-access
import asyncio
from unittest.mock import patch

import aiohttp
import pytest

from autarco import Autarco
from autarco.exceptions import (
    AutarcoAuthenticationError,
    AutarcoConnectionError,
    AutarcoConnectionTimeoutError,
    AutarcoError,
)

from . import load_fixtures


@pytest.mark.asyncio
async def test_json_request(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text='{"status": "ok"}',
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = Autarco(  # noqa: S106
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        await client._request("test")
        await client.close()


@pytest.mark.asyncio
async def test_internal_session(aresponses):
    """Test JSON response is handled correctly."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(
            status=200,
            headers={"Content-Type": "application/json"},
            text=load_fixtures("autarco.json"),
        ),
    )
    async with Autarco(  # noqa: S106
        email="test@autarco.com", password="energy"
    ) as autarco:
        await autarco._request("test")


@pytest.mark.asyncio
async def test_timeout(aresponses):
    """Test request timeout from Autarco API."""
    # Faking a timeout by sleeping
    async def response_handler(_):
        await asyncio.sleep(0.2)
        return aresponses.Response(
            body="Goodmorning!", text=load_fixtures("autarco.json")
        )

    aresponses.add("my.autarco.com", "/api/site/test", "GET", response_handler)

    async with aiohttp.ClientSession() as session:
        client = Autarco(  # noqa: S106
            email="test@autarco.com",
            password="energy",
            session=session,
            request_timeout=0.1,
        )
        with pytest.raises(AutarcoConnectionTimeoutError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_content_type(aresponses):
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

    async with aiohttp.ClientSession() as session:
        client = Autarco(  # noqa: S106
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        with pytest.raises(AutarcoError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_client_error():
    """Test request client error from Autarco API."""
    async with aiohttp.ClientSession() as session:
        client = Autarco(  # noqa: S106
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        with patch.object(
            session, "request", side_effect=aiohttp.ClientError
        ), pytest.raises(AutarcoConnectionError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_http_error400(aresponses):
    """Test HTTP 404 response handling."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(text="GIVE ME SOLARPOWER!", status=404),
    )

    async with aiohttp.ClientSession() as session:
        client = Autarco(  # noqa: S106
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        with pytest.raises(AutarcoConnectionError):
            assert await client._request("test")


@pytest.mark.asyncio
async def test_http_error401(aresponses):
    """Test HTTP 401 response handling."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(text="GIVE ME SOLARPOWER!", status=401),
    )

    async with aiohttp.ClientSession() as session:
        client = Autarco(  # noqa: S106
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        with pytest.raises(AutarcoAuthenticationError):
            assert await client._request("test")
