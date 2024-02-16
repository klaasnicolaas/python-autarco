"""Fixtures for the Autarco tests."""
from collections.abc import AsyncGenerator

import pytest
from aiohttp import ClientSession

from autarco import Autarco


@pytest.fixture(name="autarco_client")
async def client() -> AsyncGenerator[Autarco, None]:
    """Return a Autarco client."""
    async with ClientSession() as session, Autarco(
        email="test@autarco.com", password="energy", session=session
    ) as autarco_client:
        yield autarco_client
