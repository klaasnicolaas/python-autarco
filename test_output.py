# pylint: disable=W0621
"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Account, Autarco, Inverter, Solar


async def main():
    """Test."""
    async with Autarco(  # noqa: S106
        public_key="123456789",
        username="test@autarco.com",
        password="test",
    ) as autarco:
        inverters: Inverter = await autarco.all_inverters()
        solar: Solar = await autarco.solar()
        account: Account = await autarco.account()

        print("--- INVERTER(S) ---")
        print(inverters)
        print()
        for item in inverters:
            print(item)
        print()

        print("--- SOLAR ---")
        print(solar)
        print()
        print(f"Power Production: {solar.power_production}")
        print(f"Energy Production - Today: {solar.energy_production_today}")
        print(f"Energy Production - Month: {solar.energy_production_month}")
        print(f"Energy Production - Total: {solar.energy_production_total}")
        print()

        print("--- ACCOUNT ---")
        print(account)
        print()
        print(f"Public Key: {account.public_key}")
        print(f"Name: {account.name}")
        print(f"City: {account.city}")
        print(f"State: {account.state}")
        print(f"Country: {account.country}")
        print(f"Timezone: {account.timezone}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
