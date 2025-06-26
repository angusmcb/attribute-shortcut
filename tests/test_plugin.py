from qgis.core import QgsProject

from attributeshortcut.plugin import AttributeShortcutIndicator, Plugin


def test_plugin_initialization():
    Plugin()


def test_plugin_init_gui():
    plugin = Plugin()
    plugin.initGui()


def test_add_indicator_to_layers(qgis_countries_layer, qgis_iface, qgis_new_project):
    QgsProject.instance().addMapLayer(qgis_countries_layer)

    plugin = Plugin()
    plugin.initGui()

    layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(qgis_countries_layer.id())
    layer_tree_view = qgis_iface.layerTreeView()
    assert (
        sum(
            isinstance(ind, AttributeShortcutIndicator)
            for ind in layer_tree_view.indicators(layer_tree_layer)
        )
        == 1
    )


def test_add_indicator_to_layer_added_later(qgis_countries_layer, qgis_iface, qgis_new_project):
    plugin = Plugin()
    plugin.initGui()

    QgsProject.instance().addMapLayer(qgis_countries_layer)

    layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(qgis_countries_layer.id())
    layer_tree_view = qgis_iface.layerTreeView()
    assert (
        sum(
            isinstance(ind, AttributeShortcutIndicator)
            for ind in layer_tree_view.indicators(layer_tree_layer)
        )
        == 1
    )
