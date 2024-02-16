"""Models for Autarco."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from mashumaro import DataClassDictMixin, field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin


@dataclass
class PowerResponse(DataClassORJSONMixin):
    """Object representing an Inverter model response from the API."""

    inverters: dict[str, Inverter]
    stats: dict[str, dict[str, int]]


@dataclass
class EnergyResponse(DataClassORJSONMixin):
    """Object representing an Inverter model response from the API."""

    stats: dict[str, dict[str, Any]]


@dataclass
class Inverter(DataClassORJSONMixin):
    """Object representing an Inverter model response from the API."""

    serial_number: str = field(metadata=field_options(alias="sn"))
    out_ac_power: int
    out_ac_energy_total: int
    grid_turned_off: bool
    health: str


@dataclass
class Solar(DataClassDictMixin):
    """Object representing a Solar model response from the API."""

    power_production: int = field(metadata=field_options(alias="pv_now"))
    energy_production_today: int = field(metadata=field_options(alias="pv_today"))
    energy_production_month: int = field(metadata=field_options(alias="pv_month"))
    energy_production_total: int = field(metadata=field_options(alias="pv_to_date"))


@dataclass
class Account(DataClassORJSONMixin):
    """Object representing an Account model response from the API."""

    public_key: str
    name: str
    address: Address

    timezone: str
    dt_created: date = field(
        metadata=field_options(
            alias="dt_created", deserialize=lambda x: date.fromisoformat(x)
        )
    )
    has_consumption_meter: bool
    has_battery: bool


@dataclass
class Address(DataClassORJSONMixin):
    """Object representing an Address model response from the API."""

    street: str = field(metadata=field_options(alias="address_line_1"))
    zip_code: str = field(metadata=field_options(alias="postcode"))
    city: str
    country: str
