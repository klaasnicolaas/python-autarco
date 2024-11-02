"""Models for Autarco."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

from mashumaro import DataClassDictMixin, field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import SerializationStrategy


class DateStrategy(SerializationStrategy):
    """Date serialization strategy to handle the date format."""

    def serialize(self, value: date) -> str:
        """Serialize date to string."""
        return value.strftime("%Y-%m-%d")

    def deserialize(self, value: str) -> date:
        """Deserialize string to date."""
        return date.fromisoformat(value)


@dataclass
class PowerResponse(DataClassORJSONMixin):
    """Object representing an Power Response model from the API."""

    inverters: dict[str, Inverter]
    stats: Stats


@dataclass
class EnergyResponse(DataClassORJSONMixin):
    """Object representing an Energy Response model response from the API."""

    stats: Stats


@dataclass
class AccountResponse(DataClassORJSONMixin):
    """Object representing an Account Response model from the API."""

    sites: list[AccountSite] = field(metadata=field_options(alias="data"))


@dataclass
class AccountSite(DataClassORJSONMixin):
    """Object representing an Account Site model response from the API."""

    site_id: int
    public_key: str
    system_name: str = field(metadata=field_options(alias="name"))
    retailer: str = field(metadata=field_options(alias="name_retailer"))
    health: str


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
class Battery(DataClassDictMixin):
    """Object representing a Battery model response from the API."""

    # Power - Flow
    flow_now: int = field(metadata=field_options(alias="battery_now"))
    net_charged_now: int = field(
        metadata=field_options(alias="battery_net_charged_now")
    )
    state_of_charge: int = field(metadata=field_options(alias="battery_soc"))

    # Energy - Discharged
    discharged_today: int = field(
        metadata=field_options(alias="battery_discharged_today")
    )
    discharged_month: int = field(
        metadata=field_options(alias="battery_discharged_month")
    )
    discharged_total: int = field(
        metadata=field_options(alias="battery_discharged_to_date")
    )

    # Energy - Charged
    charged_today: int = field(metadata=field_options(alias="battery_charged_today"))
    charged_month: int = field(metadata=field_options(alias="battery_charged_month"))
    charged_total: int = field(metadata=field_options(alias="battery_charged_to_date"))


@dataclass
class Graphs(DataClassORJSONMixin):
    """Object representing Graphs model from the API."""

    pv_power: dict[str, dict[datetime, int | None]] | None = None
    pv_energy: dict[str, dict[date, int | None]] | None = None


@dataclass
class Stats(DataClassORJSONMixin):
    """Object representing the Stats model from the API."""

    graphs: Graphs
    kpis: dict[str, Any]

    @property
    def generate_power_stats_inverter(self) -> dict[str, list[dict[str, Any]]] | None:
        """Generate power statistics by inverter."""
        if self.graphs.pv_power:
            power_stats_by_inverter = {}
            for inverter_id, power_data in self.graphs.pv_power.items():
                stats_list = [
                    {"timestamp": timestamp, "power": power}
                    for timestamp, power in power_data.items()
                ]
                power_stats_by_inverter[inverter_id] = stats_list
            return power_stats_by_inverter
        return None

    @property
    def generate_energy_stats_inverter(self) -> dict[str, list[dict[str, Any]]] | None:
        """Generate energy statistics by inverter."""
        if self.graphs.pv_energy:
            energy_stats_by_inverter = {}
            for inverter_id, energy_data in self.graphs.pv_energy.items():
                stats_list = [
                    {"timestamp": date, "energy": energy}
                    for date, energy in energy_data.items()
                ]
                energy_stats_by_inverter[inverter_id] = stats_list
            return energy_stats_by_inverter
        return None


@dataclass
class Site(DataClassORJSONMixin):
    """Object representing an Site model response from the API."""

    # pylint: disable-next=too-few-public-methods
    class Config(BaseConfig):
        """Mashumaro configuration."""

        serialization_strategy = {date: DateStrategy()}  # noqa: RUF012
        serialize_by_alias = True

    public_key: str
    name: str
    address: Address

    has_consumption_meter: bool
    has_battery: bool
    timezone: str
    created_at: date | None = field(
        metadata=field_options(alias="dt_created"), default=None
    )


@dataclass
class Address(DataClassORJSONMixin):
    """Object representing an Address model response from the API."""

    street: str = field(metadata=field_options(alias="address_line_1"))
    zip_code: str = field(metadata=field_options(alias="postcode"))
    city: str
    country: str
