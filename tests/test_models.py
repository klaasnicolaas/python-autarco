"""Test the Autarco models."""

from datetime import date

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from autarco import Account, Autarco, DateStrategy, Inverter, Location, Solar

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


async def test_get_location(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Location object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/",
        "GET",
        aresponses.Response(
            text=load_fixtures("location.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    location: Location = await autarco_client.get_location(public_key="fake_key")
    assert location == snapshot


async def test_get_account(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Account object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/",
        "GET",
        aresponses.Response(
            text=load_fixtures("account.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    account: Account = await autarco_client.get_account()
    assert account == snapshot
    assert account.public_key == "blabla"


def test_serialize_date() -> None:
    """Test the serialization of a date object."""
    test_date = date(2021, 8, 1)
    assert DateStrategy().serialize(test_date) == "2021-08-01"
