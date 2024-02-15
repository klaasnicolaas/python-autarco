"""Test the models."""
import aiohttp
import pytest
from aresponses import ResponsesMockServer

from autarco import Account, Autarco, Inverter, Solar

from . import load_fixtures


@pytest.mark.asyncio
async def test_all_inverters(aresponses: ResponsesMockServer) -> None:
    """Test request from a Autarco API - Inverter object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/power",
        "GET",
        aresponses.Response(
            text=load_fixtures("inverters.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Autarco(
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        inverters: dict[str, Inverter] = await client.all_inverters(
            public_key="fake_key"
        )
        assert inverters is not None
        for item in inverters.values():
            assert item.serial_number
            assert item.out_ac_power == 100
            assert item.out_ac_energy_total
            assert item.grid_turned_off is False
            assert item.health == "OK"


@pytest.mark.asyncio
async def test_solar(aresponses: ResponsesMockServer) -> None:
    """Test request from a Autarco API - Solar object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/",
        "GET",
        aresponses.Response(
            text=load_fixtures("autarco.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Autarco(
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        solar: Solar = await client.solar(public_key="fake_key")
        assert solar is not None
        assert solar.power_production == 200
        assert solar.energy_production_today == 4
        assert solar.energy_production_month == 58
        assert solar.energy_production_total == 10379


@pytest.mark.asyncio
async def test_account(aresponses: ResponsesMockServer) -> None:
    """Test request from a Autarco API - Account object."""
    aresponses.add(
        "my.autarco.com",
        "/api/site/fake_key/",
        "GET",
        aresponses.Response(
            text=load_fixtures("autarco.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = Autarco(
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        account: Account = await client.account(public_key="fake_key")
        assert account is not None
        assert account.public_key == "sd6fv516"
        assert account.name == "Autarco Integration"
        assert account.city == "Amsterdam"
        assert account.state == "www"
        assert account.country == "Online"
        assert account.timezone == "Europe/Amsterdam"


@pytest.mark.asyncio
async def test_get_public_key(aresponses: ResponsesMockServer) -> None:
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

    async with aiohttp.ClientSession() as session:
        client = Autarco(
            email="test@autarco.com",
            password="energy",
            session=session,
        )
        public_key = await client.get_public_key()
        assert public_key is not None
        assert public_key == "sd6fv516"
