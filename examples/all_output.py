"""Asynchronous Python client for the Autarco API."""

import asyncio

from autarco import AccountSite, Autarco, Inverter, Site, Solar


async def main() -> None:
    """Test."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as autarco:
        account_sites: list[AccountSite] = await autarco.get_account()

        inverters: dict[str, Inverter] = await autarco.get_inverters(
            account_sites[0].public_key
        )
        solar: Solar = await autarco.get_solar(account_sites[0].public_key)
        site: Site = await autarco.get_site(account_sites[0].public_key)

        print("--- ACCOUNT ---")
        print(account_sites)
        print()
        for item in account_sites:
            print(f"Site ID: {item.site_id}")
            print(f"Public Key: {item.public_key}")
            print(f"Name: {item.system_name}")
            print(f"Retailer: {item.retailer}")
            print(f"Health: {item.health}")
        print()

        print("--- INVERTER(S) ---")
        print(inverters)
        print()
        for inverter in inverters.values():
            print(f"Serial Number: {inverter.serial_number}")
            print(f"Out AC Power: {inverter.out_ac_power}")
            print(f"Out AC Energy Total: {inverter.out_ac_energy_total}")
            print(f"Grid Turned Off: {inverter.grid_turned_off}")
            print(f"Health: {inverter.health}")
        print()

        print("--- SOLAR ---")
        print(solar)
        print()
        print(f"Power Production: {solar.power_production}")
        print(f"Energy Production - Today: {solar.energy_production_today}")
        print(f"Energy Production - Month: {solar.energy_production_month}")
        print(f"Energy Production - Total: {solar.energy_production_total}")
        print()

        print("--- SITE ---")
        print(site)
        print()
        print(f"Address: {site.address}")
        print(f"Timezone: {site.timezone}")
        print(f"Created At: {site.created_at}")
        print(f"Consumption Meter: {site.has_consumption_meter}")
        print(f"Has Battery: {site.has_battery}")


if __name__ == "__main__":
    asyncio.run(main())
