from __future__ import annotations

from typing import cast

from qgis.core import (
    QgsApplication,
    QgsLayerTreeGroup,
    QgsMapLayer,
    QgsProject,
    QgsVectorLayer,
)
from qgis.gui import (
    QgisInterface,
    QgsLayerTreeViewIndicator,
)
from qgis.utils import iface

iface = cast(QgisInterface, iface)

ATTRIBUTE_TABLE_ICON = QgsApplication.getThemeIcon("mActionOpenTable.svg")


class Plugin:
    def __init__(self) -> None:
        self.indicators: dict[str, AttributeShortcutIndicator] = {}

    def initGui(self) -> None:  # noqa N802
        project = QgsProject.instance()
        root = project.layerTreeRoot()

        project.layersAdded.connect(self.map_layers_added)
        root.addedChildren.connect(self.layer_tree_layer_added)

        existing_layers = project.mapLayers().values()
        self.map_layers_added(existing_layers)

    def unload(self) -> None:
        project = QgsProject.instance()
        root = project.layerTreeRoot()
        layer_tree_view = iface.layerTreeView()

        project.layersAdded.disconnect(self.map_layers_added)
        root.addedChildren.disconnect(self.layer_tree_layer_added)

        for layer_id, indicator in self.indicators.items():
            layer_tree_layer = root.findLayer(layer_id)
            if layer_tree_layer:
                layer_tree_view.removeIndicator(layer_tree_layer, indicator)
            indicator.deleteLater()

        self.indicators.clear()

    def map_layers_added(self, layers: list[QgsMapLayer]) -> None:
        """Receive map layers added to the project and add indicators to them."""
        root = QgsProject.instance().layerTreeRoot()

        for layer in layers:
            layer_id = layer.id()

            if layer_id in self.indicators:  # Already has an indicator
                continue
            if not isinstance(layer, QgsVectorLayer):  # Only vector layers
                continue

            indicator = AttributeShortcutIndicator(layer_id)
            self.indicators[layer_id] = indicator

            layer_tree_layer = root.findLayer(layer_id)

            if not layer_tree_layer:
                continue

            iface.layerTreeView().addIndicator(layer_tree_layer, indicator)

    def layer_tree_layer_added(
        self,
        layer_tree: QgsLayerTreeGroup,
        indexFrom: int,  # noqa: N803
        indexTo: int,  # noqa: N803
    ) -> None:
        """Receive layer tree layers added and attach indicator to them if indicator exists."""

        layer_tree_nodes = layer_tree.children()[indexFrom : indexTo + 1]

        for layer_tree_node in layer_tree_nodes:
            try:
                layer_id = layer_tree_node.layerId()
            except AttributeError:  # Not a layer node
                continue

            try:
                indicator = self.indicators[layer_id]
            except KeyError:  # No indicator for this layer
                continue

            iface.layerTreeView().addIndicator(layer_tree_node, indicator)


class AttributeShortcutIndicator(QgsLayerTreeViewIndicator):
    """Custom indicator for the attribute shortcut plugin."""

    def __init__(self, layer_id: str) -> None:
        super().__init__()
        self.layer_id = layer_id
        self.setIcon(ATTRIBUTE_TABLE_ICON)
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
