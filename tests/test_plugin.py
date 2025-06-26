import pytest
from qgis.core import QgsProject

from attributeshortcut.plugin import AttributeShortcutIndicator, Plugin


@pytest.fixture
def plugin():
    """Fixture to initialize the plugin."""
    plugin = Plugin()
    plugin.initGui()
    yield plugin
    plugin.unload()


def test_plugin_initialization():
    Plugin()


def test_plugin_init_gui_and_unload():
    plugin = Plugin()
    plugin.initGui()
    plugin.unload()


def test_add_indicator_to_existing_layers(qgis_countries_layer, qgis_iface, qgis_new_project):
    QgsProject.instance().addMapLayer(qgis_countries_layer)

    plugin = Plugin()
    plugin.initGui()

    layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(qgis_countries_layer.id())
    layer_tree_view = qgis_iface.layerTreeView()
    indicators = layer_tree_view.indicators(layer_tree_layer)
    assert sum(isinstance(ind, AttributeShortcutIndicator) for ind in indicators) == 1
    plugin.unload()


def test_add_indicator_to_layer_added_later(
    qgis_countries_layer, qgis_iface, plugin, qgis_new_project
):
    QgsProject.instance().addMapLayer(qgis_countries_layer)

    layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(qgis_countries_layer.id())
    layer_tree_view = qgis_iface.layerTreeView()
    indicators = layer_tree_view.indicators(layer_tree_layer)
    assert sum(isinstance(ind, AttributeShortcutIndicator) for ind in indicators) == 1
