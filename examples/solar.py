"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Account, Autarco


async def main() -> None:
    """Show example on getting Autarco - solar data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account: Account = await client.get_account()
        solar = await client.get_solar(account.public_key)
        print(solar)


if __name__ == "__main__":
    asyncio.run(main())
