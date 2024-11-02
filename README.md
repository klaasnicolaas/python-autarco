<!-- Banner -->
![alt Banner of the Autarco package](https://raw.githubusercontent.com/klaasnicolaas/python-autarco/main/assets/header_autarco-min.png)

<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![PyPi Downloads][downloads-shield]][downloads-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]
[![Open in Dev Containers][devcontainer-shield]][devcontainer]

[![Build Status][build-shield]][build-url]
[![Typing Status][typing-shield]][typing-url]
[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]

Asynchronous Python client for the Autarco Inverters (External API).

## About

A python package with which you can read the data of your [Autarco][autarco]
Inverter(s). This is done by making a request to the [My Autarco][my-autarco]
platform, for this you will need the `email` and `password`.
The data on the platform is updated every 5 minutes.

### Public key

You can find this in the url after logging in,
example: `https://my.autarco.com/site/{public_key}`

Or by using the `get_account` function, and use the `public_key` attribute.

## Installation

```bash
pip install autarco
```

## Usage

```python
import asyncio

from autarco import Autarco


async def main():
    """Show example on getting Autarco data."""
    async with Autarco(
        email="test@autarco.com",
        password="password",
    ) as client:
        account_sites = await client.get_account()

        inverters = await client.get_inverters(account_sites[0].public_key)
        battery = await client.get_battery(account_sites[0].public_key)
        solar = await client.get_solar(account_sites[0].public_key)
        site = await client.get_site(account_sites[0].public_key)
        print(inverters)
        print(battery)
        print(solar)
        print(site)


if __name__ == "__main__":
    asyncio.run(main())
```

More examples can be found in the [examples folder](./examples/).

## Datasets

You can read the following with this package:

- **Account** data with all the sites you have access to.
- **Inverter(s)** data with the power output, energy output, grid status and health status.
- **Solar** data with the power production, energy production of today, this month and total.
- **Battery** data with insights into your batteries.
- **Site** general information about a specific site.
- **Statistics** of the inverter(s) with power and energy data.

<details>
  <summary>CLICK HERE! to see all dataset details</summary>

### Account

With all the sites you have access to.

| Name          | Type  | Description                        |
| :------------ | :---- | :--------------------------------- |
| `site_id`     | `str` | The unique identifier of the site. |
| `public_key`  | `str` | The public key of the site.        |
| `system_name` | `str` | The name of the site system.       |
| `retailer`    | `str` | The name of the retailer.          |
| `health`      | `str` | The health status of the site.     |

### Inverter(s)

| Name                  | Type    | Description                                     |
| :-------------------- | :------ | :---------------------------------------------- |
| `serial_number`       | `str`   | The serial number of the inverter.              |
| `out_ac_power`        | `int`   | The power output of the inverter in W.          |
| `out_ac_energy_total` | `float` | The total energy output of the inverter in kWh. |
| `grid_turned_off`     | `bool`  | If the grid is turned off.                      |
| `health`              | `str`   | The health status of the inverter.              |

### Solar

| Name                      | Type    | Description                                 |
| :------------------------ | :------ | :------------------------------------------ |
| `power_production`        | `int`   | The current power production in W.          |
| `energy_production_today` | `float` | The energy production of today in kWh.      |
| `energy_production_month` | `float` | The energy production of this month in kWh. |
| `energy_production_total` | `float` | The total energy production in kWh.         |

### Battery

| Name              | Type  | Description                                                       |
| :-----------------| :---- | :---------------------------------------------------------------- |
| `flow_now`        | `int` | The current battery flow in W.                                    |
| `net_charged_now` | `int` | The current net charged battery in W.                             |
| `state_of_charge` | `int` | The current state of charge of the battery in %.                  |
| `discharged_today`| `int` | How much energy the battery has discharged **today** in kWh.      |
| `discharged_month`| `int` | How much energy the battery has discharged this **month** in kWh. |
| `discharged_total`| `int` | How much energy the battery has discharged in **total** in kWh.   |
| `charged_today`   | `int` | How much energy the battery has charged **today** in kWh.         |
| `charged_month`   | `int` | How much energy the battery has charged this **month** in kWh.    |
| `charged_total`   | `int` | How much energy the battery has charged in **total** in kWh.      |

### Site

| Name                    | Type   | Description                                                                   |
| :---------------------- | :----- | :---------------------------------------------------------------------------- |
| `public_key`            | `str`  | The public key of the site.                                                   |
| `name`                  | `str`  | The name of the site.                                                         |
| `address`               | `dict` | The address of the site. (**street**, **zip code**, **city** and **country**) |
| `has_consumption_meter` | `bool` | If the site has a consumption meter.                                          |
| `timezone`              | `str`  | The timezone of the site.                                                     |
| `has_battery`           | `bool` | If the site has a battery.                                                    |
| `created_at`            | `date` | The creation date of the site. (default: None)                                |

### Statistics

It is possible to retrieve inverter(s) statistical data from the API, a distinction has been made into two types:

#### Power

Parameters to get the **power** statistics of the site.

- **query_range** (default: `day`) - The range of the query, can be `day` or `week`.

| Name                | Type   | Description                             |
| :------------------ | :----- | :-------------------------------------- |
| `graphs`.`pv_power` | `dict` | The power statistics for each inverter. |

You can generate a better list with the property `generate_power_stats_inverter` of the `Stats` object.

#### Energy

Parameters to get the **energy** statistics of the site.

- **query_range** (default: `month`) - The range of the query, can be `month`, `year` or `total`.

| Name                 | Type   | Description                              |
| :------------------- | :----- | :--------------------------------------- |
| `graphs`.`pv_energy` | `dict` | The energy statistics for each inverter. |

You can generate a better list with the property `generate_energy_stats_inverter` of the `Stats` object.

</details>

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

The simplest way to begin is by utilizing the [Dev Container][devcontainer]
feature of Visual Studio Code or by opening a CodeSpace directly on GitHub.
By clicking the button below you immediately start a Dev Container in Visual Studio Code.

[![Open in Dev Containers][devcontainer-shield]][devcontainer]

This Python project relies on [Poetry][poetry] as its dependency manager,
providing comprehensive management and control over project dependencies.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]

### Installation

Install all packages, including all development requirements:

```bash
poetry install
```

_Poetry creates by default an virtual environment where it installs all
necessary pip packages_.

### Pre-commit

This repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. To setup the pre-commit check, run:

```bash
poetry run pre-commit install
```

And to run all checks and tests manually, use the following command:

```bash
poetry run pre-commit run --all-files
```

### Testing

It uses [pytest](https://docs.pytest.org/en/stable/) as the test framework. To run the tests:

```bash
poetry run pytest
```

To update the [syrupy](https://github.com/tophat/syrupy) snapshot tests:

```bash
poetry run pytest --snapshot-update
```

## License

MIT License

Copyright (c) 2022-2024 Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<!-- PROJECT -->
[autarco]: https://www.autarco.com
[my-autarco]: https://my.autarco.com

<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/klaasnicolaas/python-autarco/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-autarco/actions/workflows/tests.yaml
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-autarco/branch/main/graph/badge.svg?token=JM72C3T2AT
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-autarco
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-autarco.svg
[commits-url]: https://github.com/klaasnicolaas/python-autarco/commits/master
[devcontainer-shield]: https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode
[devcontainer]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/klaasnicolaas/python-autarco
[downloads-shield]: https://img.shields.io/pypi/dm/autarco
[downloads-url]: https://pypistats.org/packages/autarco
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-autarco.svg
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-autarco.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/d38cdaa8625b6657d40b/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-autarco/maintainability
[maintenance-shield]: https://img.shields.io/maintenance/yes/2024.svg
[project-stage-shield]: https://img.shields.io/badge/project%20stage-production%20ready-brightgreen.svg
[pypi]: https://pypi.org/project/autarco/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/autarco
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-autarco.svg
[releases]: https://github.com/klaasnicolaas/python-autarco/releases
[typing-shield]: https://github.com/klaasnicolaas/python-autarco/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/klaasnicolaas/python-autarco/actions/workflows/typing.yaml

<!-- Development -->
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
