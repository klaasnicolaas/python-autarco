"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import AccountSite, Autarco


async def main() -> None:
    """Show example on getting Autarco - inverters data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account_sites: list[AccountSite] = await client.get_account()
        inverters = await client.get_inverters(account_sites[0].public_key)
        print(inverters)


if __name__ == "__main__":
    asyncio.run(main())
