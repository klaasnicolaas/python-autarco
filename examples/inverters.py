"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Autarco


async def main() -> None:
    """Show example on getting Autarco - inverters data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        public_key = await client.get_public_key()
        inverters = await client.all_inverters(public_key)
        print(inverters)


if __name__ == "__main__":
    asyncio.run(main())
