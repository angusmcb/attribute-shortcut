Development of attribute-shortcut plugin
===========================



The code for the plugin is in the [attributeshortcut](../attribute-shortcut) folder. Make sure you have required tools, such as
Qt with Qt Editor and Qt Linquist installed by following this
[tutorial](https://www.qgistutorials.com/en/docs/3/building_a_python_plugin.html#get-the-tools).



## Keeping dependencies up to date

1. Activate the virtual environment.
2. `pip install pip-tools`
3. `pip-compile --upgrade requirements-dev.in`
4. `pip install -r requirements-dev.txt` or `pip-sync requirements-dev.txt`

## Adding or editing  source files

If you create or edit source files make sure that:

* they contain absolute imports:
    ```python
    from attributeshortcut.utils.exceptions import TestException # Good

    from ..utils.exceptions import TestException # Bad

    ```
* you consider adding test files for the new functionality

## Testing

Install python packages listed in [requirements-dev.txt](../requirements-dev.txt) to the virtual environment
and run tests with:

```shell script
pytest
```

## Translating

### Translating with Transifex

Fill in `transifex_coordinator` (Transifex username) and `transifex_organization`
in [.qgis-plugin-ci](../.qgis-plugin-ci) to use Transifex translation.

If you want to see the translations during development, add `i18n` to the `extra_dirs` in `build.py`:

```python
extra_dirs = ["resources", "i18n"]
```

#### Pushing / creating new translations

For step-by-step instructions, read the [translation tutorial](./translation_tutorial.md#Tutorial).

* First, install [Transifex CLI](https://docs.transifex.com/client/installing-the-client) and
  [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci)
* Make sure command `pylupdate5` works. Otherwise install it with `pip install pyqt5`
* Run `qgis-plugin-ci push-translation <your-transifex-token>`
* Go to your Transifex site, add some languages and start translating
* Copy [push_translations.yml](push_translations.yml) file to [workflows](../.github/workflows) folder to enable
  automatic pushing after commits to master
* Add this badge ![](https://github.com/angusmcb/attribute-shortcut/workflows/Translations/badge.svg) to
  the [README](../README.md)

##### Pulling

There is no need to pull if you configure `--transifex-token` into your
[release](../.github/workflows/release.yml) workflow (remember to use Github Secrets). Remember to uncomment the
lrelease section as well. You can however pull manually to test the process.

* Run `qgis-plugin-ci pull-translation --compile <your-transifex-token>`

### Github Release

Follow these steps to create a release

* Add changelog information to [CHANGELOG.md](../CHANGELOG.md) using this
  [format](https://raw.githubusercontent.com/opengisch/qgis-plugin-ci/master/CHANGELOG.md)
* Make a new commit. (`git add -A && git commit -m "Release 0.1.0"`)
* Create new tag for it (`git tag -a 0.1.0 -m "Version 0.1.0"`)
* Push tag to Github using `git push --follow-tags`
* Create Github release
* [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci) adds release zip automatically as an asset

Modify [release](../.github/workflows/release.yml) workflow according to its comments if you want to upload the
plugin to QGIS plugin repository.

### Local release

For local release install [qgis-plugin-ci](https://github.com/opengisch/qgis-plugin-ci) (possibly to different venv
to avoid Qt related problems on some environments) and follow these steps:
```shell
cd attribute-shortcut
qgis-plugin-ci package --disable-submodule-update 0.1.0
```
