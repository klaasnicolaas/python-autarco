"""Models for Autarco."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Inverter:
    """Object representing an Inverter model response from the API."""

    serial_number: str
    out_ac_power: int
    out_ac_energy_total: int
    grid_turned_off: bool
    health: str

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Inverter:
        """Create an Inverter object from a JSON response.

        Args:
            data: JSON response from the API.

        Returns:
            An Inverter object.
        """
        data = data[1]
        return cls(
            serial_number=data.get("sn"),
            out_ac_power=data.get("out_ac_power"),
            out_ac_energy_total=data.get("out_ac_energy_total"),
            grid_turned_off=data.get("grid_turned_off"),
            health=data.get("health"),
        )


@dataclass
class Solar:
    """Object representing a Solar model response from the API."""

    power_production: int
    energy_production_today: int
    energy_production_month: int
    energy_production_total: int

    @staticmethod
    def from_json(data: dict[str, Any]) -> Solar:
        """Create an Solar object from a JSON response.

        Args:
            data: JSON response from the API.

        Returns:
            An Solar object.
        """
        data = data["stats"]["kpis"]
        return Solar(
            power_production=data.get("current_production"),
            energy_production_today=data.get("output_today"),
            energy_production_month=data.get("output_month"),
            energy_production_total=data.get("output_to_date"),
        )


@dataclass
class Account:
    """Object representing an Account model response from the API."""

    public_key: str
    name: str
    city: str
    state: str
    country: str
    timezone: str

    @staticmethod
    def from_json(data: dict[str, Any]) -> Account:
        """Create an Account object from a JSON response.

        Args:
            data: JSON response from the API.

        Returns:
            An Account object.
        """
        data = data["site"]
        address = data["address"]
        return Account(
            public_key=data.get("public_key"),
            name=data.get("name"),
            city=address.get("city"),
            state=address.get("state"),
            country=address.get("country"),
            timezone=data.get("timezone"),
        )
