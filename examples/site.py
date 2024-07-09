"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import AccountSite, Autarco


async def main() -> None:
    """Show example on getting Autarco - site data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account_sites: list[AccountSite] = await client.get_account()
        site = await client.get_site(account_sites[0].public_key)
        print(site)


if __name__ == "__main__":
    asyncio.run(main())
