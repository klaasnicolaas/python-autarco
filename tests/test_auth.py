"""Auth tests for Autarcp."""

# pylint: disable=protected-access
import pytest
from aresponses import ResponsesMockServer

from autarco import Autarco
from autarco.exceptions import AutarcoAuthenticationError


async def test_authentication_error(
    aresponses: ResponsesMockServer,
    autarco_client: Autarco,
) -> None:
    """Test authentication error is handled correctly."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/test",
        "GET",
        aresponses.Response(status=401),
    )
    with pytest.raises(AutarcoAuthenticationError):
        assert await autarco_client._request("test")
