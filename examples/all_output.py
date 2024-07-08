"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import Account, Autarco, Inverter, Location, Solar


async def main() -> None:
    """Test."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as autarco:
        account: Account = await autarco.get_account()

        inverters: dict[str, Inverter] = await autarco.get_inverters(account.public_key)
        solar: Solar = await autarco.get_solar(account.public_key)
        location: Location = await autarco.get_location(account.public_key)

        print("--- ACCOUNT ---")
        print(account)
        print()
        print(f"Public Key: {account.public_key}")
        print(f"Name: {account.system_name}")
        print(f"Retailer: {account.retailer}")
        print(f"Health: {account.health}")

        print("--- INVERTER(S) ---")
        print(inverters)
        print()
        for item in inverters.values():
            print(f"Serial Number: {item.serial_number}")
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

        print("--- LOCATION ---")
        print(location)
        print()
        print(f"Address: {location.address}")
        print(f"Timezone: {location.timezone}")
        print(f"Created At: {location.created_at}")
        print(f"Consumption Meter: {location.has_consumption_meter}")
        print(f"Has Battery: {location.has_battery}")


if __name__ == "__main__":
    asyncio.run(main())
