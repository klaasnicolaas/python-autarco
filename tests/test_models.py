"""Test the Autarco models."""
from aiohttp import ClientSession
from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from autarco import Account, Autarco, Inverter, Solar

from . import load_fixtures


async def test_get_inverters(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Inverter object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/power",
        "GET",
        aresponses.Response(
            text=load_fixtures("power.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    inverters: dict[str, Inverter] = await autarco_client.get_inverters(
        public_key="fake_key"
    )
    assert inverters == snapshot


async def test_get_solar(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Solar object."""
    # Energy response
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/energy",
        "GET",
        aresponses.Response(
            text=load_fixtures("energy.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    # Power response
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/power",
        "GET",
        aresponses.Response(
            text=load_fixtures("power.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    solar: Solar = await autarco_client.get_solar(public_key="fake_key")
    assert solar == snapshot


async def test_get_account(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Account object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/",
        "GET",
        aresponses.Response(
            text=load_fixtures("account.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    account: Account = await autarco_client.get_account(public_key="fake_key")
    assert account == snapshot


async def test_get_public_key(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - get_public_key."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/",
        "GET",
        aresponses.Response(
            text=load_fixtures("public_key.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    public_key = await autarco_client.get_public_key()
    assert public_key == snapshot
    assert public_key == "sd6fv516"
