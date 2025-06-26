from __future__ import annotations

from typing import Any, cast

from qgis.core import (
    QgsApplication,
    QgsLayerTree,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsMapLayer,
    QgsProject,
    QgsVectorLayer,
)
from qgis.gui import (
    QgisInterface,
    QgsLayerTreeView,
    QgsLayerTreeViewIndicator,
)
from qgis.utils import iface

iface = cast(QgisInterface, iface)


class Plugin:
    def __init__(self) -> None:
        self.indicators: dict[str, AttributeShortcutIndicator] = {}

    def initGui(self) -> None:  # noqa N802
        project = QgsProject.instance()

        project.layersAdded.connect(self.receive_layers_added)

        root = project.layerTreeRoot()
        root.addedChildren.connect(self.layer_tree_layer_added)

        existing_layers = project.mapLayers().values()
        self.receive_layers_added(existing_layers)

    def unload(self) -> None:
        project = QgsProject.instance()

        project.layersAdded.disconnect(self.receive_layers_added)

        root = project.layerTreeRoot()
        root.addedChildren.disconnect(self.layer_tree_layer_added)

        for layer_id, indicator in self.indicators.items():
            layer_tree_layer = project.layerTreeRoot().findLayer(layer_id)
            if layer_tree_layer:
                iface.layerTreeView().removeIndicator(layer_tree_layer, indicator)
            indicator.deleteLater()

        self.indicators.clear()

    def receive_layers_added(self, layers: list[QgsMapLayer]) -> None:
        """Receive layers added to the project and add indicators to them."""

        for layer in layers:
            layer_id = layer.id()

            if layer_id in self.indicators:
                continue
            if not isinstance(layer, QgsVectorLayer):
                continue

            indicator = AttributeShortcutIndicator(layer_id)
            self.indicators[layer_id] = indicator

            layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(layer_id)

            if not layer_tree_layer:
                continue

            iface.layerTreeView().addIndicator(layer_tree_layer, indicator)

    def layer_tree_layer_added(self, layer_tree: QgsLayerTreeGroup, *args: Any) -> None:
        for layer_tree_layer in layer_tree.findLayers():
            layer_id = layer_tree_layer.layerId()

            if layer_id not in self.indicators:
                continue

            indicator = self.indicators[layer_id]
            iface.layerTreeView().addIndicator(layer_tree_layer, indicator)


class AttributeShortcutIndicator(QgsLayerTreeViewIndicator):
    """Custom indicator for the attribute shortcut plugin."""

    _icon = QgsApplication.getThemeIcon("mActionOpenTable.svg")

    def __init__(self, layer_id: str) -> None:
        super().__init__()
        self.layer_id = layer_id
        self.setIcon(self._icon)
        # Aim to borrow translation from qgis core
        self.setToolTip(
            QgsApplication.translate("QgsMapToolIdentifyAction", "Show Attribute Table")
        )
        self.clicked.connect(self.show_attribute_table)

    def show_attribute_table(self) -> None:
        """Show the attribute table for the layer."""
        layers = QgsProject.instance().mapLayers()
        try:
            layer = layers[self.layer_id]
        except KeyError:
            return
        iface.showAttributeTable(layer)
