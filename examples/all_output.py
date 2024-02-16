"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Account, Autarco, Inverter, Solar


async def main() -> None:
    """Test."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as autarco:
        public_key = await autarco.get_public_key()

        inverters: dict[str, Inverter] = await autarco.get_inverters(public_key)
        solar: Solar = await autarco.get_solar(public_key)
        account: Account = await autarco.get_account(public_key)

        print(f"Public key: {public_key}")
        print()

        print("--- INVERTER(S) ---")
        print(inverters)
        print()
        for item in inverters.values():
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
        print(f"Timezone: {account.timezone}")
        print(f"City: {account.address.city}")
        print(f"Country: {account.address.country}")


if __name__ == "__main__":
    asyncio.run(main())
