"""Test the Autarco models."""

from datetime import date

from aresponses import ResponsesMockServer
from syrupy.assertion import SnapshotAssertion

from autarco import (
    AccountSite,
    Autarco,
    Battery,
    DateStrategy,
    Inverter,
    Site,
    Solar,
    Stats,
)

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
        "/api/site/fake_key/kpis/energy",
        "GET",
        aresponses.Response(
            text=load_fixtures("kpis_energy.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    # Power response
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/kpis/power",
        "GET",
        aresponses.Response(
            text=load_fixtures("kpis_power.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    solar: Solar = await autarco_client.get_solar(public_key="fake_key")
    assert solar == snapshot


async def test_get_battery(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Battery object."""
    # Energy response
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/kpis/energy",
        "GET",
        aresponses.Response(
            text=load_fixtures("battery/kpis_energy.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    # Power response
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/kpis/power",
        "GET",
        aresponses.Response(
            text=load_fixtures("battery/kpis_power.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    battery: Battery = await autarco_client.get_battery(public_key="fake_key")
    assert battery == snapshot


async def test_get_site(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Site object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/",
        "GET",
        aresponses.Response(
            text=load_fixtures("site.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    # Energy response used to enrich Site with CO2/consumption
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/kpis/energy",
        "GET",
        aresponses.Response(
            text=load_fixtures("kpis_energy.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    site: Site = await autarco_client.get_site(public_key="fake_key")
    assert site == snapshot


async def test_get_old_site(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - old Site object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/",
        "GET",
        aresponses.Response(
            text=load_fixtures("old_site.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    # Energy response used to enrich Site with CO2/consumption
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/kpis/energy",
        "GET",
        aresponses.Response(
            text=load_fixtures("kpis_energy.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    site: Site = await autarco_client.get_site(public_key="fake_key")
    assert site == snapshot


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
    account_sites: list[AccountSite] = await autarco_client.get_account()
    assert account_sites == snapshot
    assert account_sites[0].public_key == "site_key_1"
    assert account_sites[1].public_key == "site_key_2"


async def test_power_statistics(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Power statistics data."""
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
    power_stats: Stats = await autarco_client.get_power_statistics(
        public_key="fake_key", query_range="day"
    )
    generator = power_stats.generate_power_stats_inverter
    assert power_stats == snapshot
    assert generator == snapshot
    assert power_stats.generate_energy_stats_inverter is None


async def test_energy_statistics(
    aresponses: ResponsesMockServer,
    snapshot: SnapshotAssertion,
    autarco_client: Autarco,
) -> None:
    """Test request from a Autarco API - Energy statistics data."""
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
    energy_stats: Stats = await autarco_client.get_energy_statistics(
        public_key="fake_key", query_range="month"
    )
    generator = energy_stats.generate_energy_stats_inverter
    assert energy_stats == snapshot
    assert generator == snapshot
    assert energy_stats.generate_power_stats_inverter is None


def test_serialize_date() -> None:
    """Test the serialization of a date object."""
    test_date = date(2021, 8, 1)
    assert DateStrategy().serialize(test_date) == "2021-08-01"
