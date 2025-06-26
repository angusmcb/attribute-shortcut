# Attribute Table Shortcut
![tests](https://github.com/angusmcb/attribute-shortcut/workflows/Tests/badge.svg)
[![codecov.io](https://codecov.io/github/angusmcb/attribute-shortcut/coverage.svg?branch=main)](https://codecov.io/github/angusmcb/attribute-shortcut?branch=main)
![release](https://github.com/angusmcb/attribute-shortcut/workflows/Release/badge.svg)

[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

## Description

Attribute Table Shortcut is a QGIS plugin that provides quick access buttons next to each layer in the layers list to open their attribute tables. This small plugin streamlines your workflow by eliminating the need to right-click layers or navigate through menus to access attribute data.

### Features

- Adds convenient buttons directly in the layers panel
- One-click access to attribute tables for any layer
- Streamlined workflow for attribute data management
- Lightweight and efficient plugin design

## Development

Create a virtual environment activate it and install needed dependencies with the following commands:
```console
python create_qgis_venv.py
.venv\Scripts\activate # On Linux and macOS run `source .venv\bin\activate`
pip install -r requirements-dev.txt
```

For more detailed development instructions see [development](docs/development.md).

### Testing the plugin on QGIS

A symbolic link / directory junction should be made to the directory containing the installed plugins pointing to the dev plugin package.

On Windows Command promt
```console
mklink /J %AppData%\QGIS\QGIS3\profiles\default\python\plugins\attributeshortcut .\attributeshortcut
```

On Windows PowerShell
```console
New-Item -ItemType SymbolicLink -Path ${env:APPDATA}\QGIS\QGIS3\profiles\default\python\plugins\attributeshortcut -Value ${pwd}\attributeshortcut
```

On Linux
```console
ln -s attributeshortcut/ ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/attributeshortcut
```

After that you should be able to enable the plugin in the QGIS Plugin Manager.

### VsCode setup

On VS Code use the workspace [attribute-shortcut.code-workspace](attribute-shortcut.code-workspace).
The workspace contains all the settings and extensions needed for development.

Select the Python interpreter with Command Palette (Ctrl+Shift+P). Select `Python: Select Interpreter` and choose
the one with the path `.venv\Scripts\python.exe`.


### Keeping dependencies up to date

1. Activate the virtual environment.
2. `pip install pip-tools`
3. `pip-compile --upgrade requirements-dev.in`
4. `pip install -r requirements-dev.txt` or `pip-sync requirements-dev.txt`

### Adding or editing  source files

If you create or edit source files make sure that:

* they contain absolute imports:
    ```python
    from attributeshortcut.utils.exceptions import TestException # Good

    from ..utils.exceptions import TestException # Bad

    ```
* you consider adding test files for the new functionality

### Testing

Install python packages listed in [requirements-dev.txt](../requirements-dev.txt) to the virtual environment
and run tests with:

```shell script
pytest
```


## License
This plugin is distributed under the terms of the [GNU General Public License, version 3](https://www.gnu.org/licenses/gpl-3.0.html) license.

See [LICENSE](LICENSE) for more information.
