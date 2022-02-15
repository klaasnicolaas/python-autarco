## Python - Autarco Client

<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]

[![Code Quality][code-quality-shield]][code-quality]
[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]
[![Build Status][build-shield]][build-url]

Asynchronous Python client for the Autarco Inverters.

## About

A python package with which you can read the data of your [Autarco][autarco]
Inverter(s). This is done by making a request to the [My Autarco][my-autarco]
platform, for this you will need the `public_key`, `username` and `password`.
The data on the platform is updated every 5 minutes.

### Public key

You can find this in the url after logging in,
example: `https://my.autarco.com/site/{public_key}`

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
        public_key="key",
        username="autarco@test.com",
        password="password",
    ) as client:
        inverters = await client.all_inverter()
        solar = await client.solar()
        account = await client.account()
        print(inverters)
        print(solar)
        print(account)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Data

You can read the following data with this package:

### Inverter(s)

- Serial Number
- Current Power Production (W)
- Total Energy Production (kWh)
- Health Status

### Solar

- Current Power Production (W)
- Energy Production - Today (kWh)
- Energy Production - Month (kWh)
- Energy Production - Total (kWh)

### Account

- Public Key (str)
- Name (str)
- City (str)
- State (str)
- Country (str)
- Timezone (str)

## Setting up development environment

This Python project is fully managed using the [Poetry][poetry] dependency
manager.

You need at least:

- Python 3.9+
- [Poetry][poetry-install]

Install all packages, including all development requirements:

```bash
poetry install
```

Poetry creates by default an virtual environment where it installs all
necessary pip packages, to enter or exit the venv run the following commands:

```bash
poetry shell
exit
```

Setup the pre-commit check, you must run this inside the virtual environment:

```bash
pre-commit install
```

*Now you're all set to get started!*

As this repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```

## License

MIT License

Copyright (c) 2022 Klaas Schoute

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
[code-quality-shield]: https://img.shields.io/lgtm/grade/python/g/klaasnicolaas/python-autarco.svg?logo=lgtm&logoWidth=18
[code-quality]: https://lgtm.com/projects/g/klaasnicolaas/python-autarco/context:python
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-autarco.svg
[commits-url]: https://github.com/klaasnicolaas/python-autarco/commits/master
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-autarco/branch/master/graph/badge.svg?token=VQTR24YFQ9
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-autarco
[forks-shield]: https://img.shields.io/github/forks/klaasnicolaas/python-autarco.svg
[forks-url]: https://github.com/klaasnicolaas/python-autarco/network/members
[issues-shield]: https://img.shields.io/github/issues/klaasnicolaas/python-autarco.svg
[issues-url]: https://github.com/klaasnicolaas/python-autarco/issues
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-autarco.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-autarco.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2022.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/443c476612a574d82467/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-autarco/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[pypi]: https://pypi.org/project/autarco/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/autarco
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-autarco.svg
[releases]: https://github.com/klaasnicolaas/python-autarco/releases
[stars-shield]: https://img.shields.io/github/stars/klaasnicolaas/python-autarco.svg
[stars-url]: https://github.com/klaasnicolaas/python-autarco/stargazers

<!-- Development -->
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
