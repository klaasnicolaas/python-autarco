"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Account, Autarco


async def main() -> None:
    """Show example on getting Autarco - location data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account: Account = await client.get_account()
        location = await client.get_location(account.public_key)
        print(location)


if __name__ == "__main__":
    asyncio.run(main())
