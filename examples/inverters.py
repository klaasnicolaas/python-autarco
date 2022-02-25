# pylint: disable=W0621
"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Autarco


async def main() -> None:
    """Show example on getting Autarco - inverters data."""
    async with Autarco(  # noqa: S106
        email="test@autarco.com",
        password="password",
    ) as client:
        public_key = await client.get_public_key()
        inverters = await client.all_inverters(public_key)
        print(inverters)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
