"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import AccountSite, Autarco


async def main() -> None:
    """Show example on getting Autarco - account data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account: list[AccountSite] = await client.get_account()
        print(account)


if __name__ == "__main__":
    asyncio.run(main())
