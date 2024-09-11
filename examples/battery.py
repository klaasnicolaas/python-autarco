"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import AccountSite, Autarco, Battery


async def main() -> None:
    """Show example on getting Autarco - battery data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account_sites: list[AccountSite] = await client.get_account()
        battery: Battery = await client.get_battery(account_sites[0].public_key)
        print(battery)


if __name__ == "__main__":
    asyncio.run(main())
