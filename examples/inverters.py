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
        power = await client.get_power_statistics(
            account_sites[0].public_key,
            query_range="day",
        )
        energy = await client.get_energy_statistics(
            account_sites[0].public_key,
            query_range="month",
        )

        print("--- INVERTERS ---")
        print(inverters)
        print()

        print("--- POWER STATS ---")
        print(power.generate_power_stats_inverter)
        print()

        print("--- ENERGY STATS ---")
        print(energy.generate_energy_stats_inverter)


if __name__ == "__main__":
    asyncio.run(main())
