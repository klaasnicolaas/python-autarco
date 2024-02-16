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

Asynchronous Python client for the Autarco Inverters.

## About

A python package with which you can read the data of your [Autarco][autarco]
Inverter(s). This is done by making a request to the [My Autarco][my-autarco]
platform, for this you will need the `email` and `password`.
The data on the platform is updated every 5 minutes.

### Public key

You can find this in the url after logging in,
example: `https://my.autarco.com/site/{public_key}`

Or by using the `get_public_key` method, that will
return your key.

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
        public_key = await client.get_public_key()

        inverters = await client.all_inverters(public_key)
        solar = await client.solar(public_key)
        account = await client.account(public_key)
        print(inverters)
        print(solar)
        print(account)


if __name__ == "__main__":
    asyncio.run(main())
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
- Address (dict)
  - Street (str)
  - Zip Code (str)
  - City (str)
  - Country (str)
- Timezone (str)
- Created At (date)
- Has consumption meter (bool)
- Has battery (bool)

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
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
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
