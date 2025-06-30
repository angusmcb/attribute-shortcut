from __future__ import annotations

from typing import cast

from qgis.core import (
    QgsApplication,
    QgsLayerTreeNode,
    QgsMapLayer,
    QgsProject,
    QgsVectorLayer,
)
from qgis.gui import (
    QgisInterface,
    QgsLayerTreeViewIndicator,
)
from qgis.PyQt.QtCore import QCoreApplication, QObject, pyqtSlot
from qgis.utils import iface

iface = cast(QgisInterface, iface)

ATTRIBUTE_TABLE_ICON = QgsApplication.getThemeIcon("mActionOpenTable.svg")

# Aim to borrow translation from qgis core
ATTRIBUTE_TABLE_TOOLTIP = QCoreApplication.translate(
    "QgsMapToolIdentifyAction", "Show Attribute Table"
)


class Plugin(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.indicators: dict[str, AttributeShortcutIndicator] = {}

    def initGui(self) -> None:  # noqa N802
        project = QgsProject.instance()
        root = project.layerTreeRoot()

        project.layerWasAdded.connect(self.map_layer_added)
        project.layerWillBeRemoved.connect(self.map_layer_will_be_removed)
        root.addedChildren.connect(self.layer_tree_layer_added)
        root.willRemoveChildren.connect(self.layer_tree_layer_will_be_removed)

        for layer in project.mapLayers().values():
            self.map_layer_added(layer)

    def unload(self) -> None:
        project = QgsProject.instance()
        root = project.layerTreeRoot()

        project.layerWasAdded.disconnect(self.map_layer_added)
        project.layerWillBeRemoved.disconnect(self.map_layer_will_be_removed)
        root.addedChildren.disconnect(self.layer_tree_layer_added)
        root.willRemoveChildren.disconnect(self.layer_tree_layer_will_be_removed)

        for layer_id in self.indicators:
            self.map_layer_will_be_removed(layer_id)

    @pyqtSlot("QgsMapLayer*")
    def map_layer_added(self, layer: QgsMapLayer) -> None:
        """Receive map layers added to the project and add indicators to them."""

        if not isinstance(layer, QgsVectorLayer):  # Only vector layers
            return

        layer_id = layer.id()

        try:
            indicator = self.indicators[layer_id]
        except KeyError:
            indicator = AttributeShortcutIndicator(layer_id)
            self.indicators[layer_id] = indicator

        layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(layer_id)

        if not layer_tree_layer:
            return

        iface.layerTreeView().addIndicator(layer_tree_layer, indicator)

    @pyqtSlot(str)
    def map_layer_will_be_removed(self, layer_id: str) -> None:
        try:
            indicator = self.indicators[layer_id]
        except KeyError:
            return

        layer_tree_layer = QgsProject.instance().layerTreeRoot().findLayer(layer_id)

        if layer_tree_layer:
            iface.layerTreeView().removeIndicator(layer_tree_layer, indicator)

        del self.indicators[layer_id]

        indicator.deleteLater()

    @pyqtSlot(QgsLayerTreeNode, int, int)
    def layer_tree_layer_added(
        self,
        layer_tree: QgsLayerTreeNode,
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

    @pyqtSlot(QgsLayerTreeNode, int, int)
    def layer_tree_layer_will_be_removed(
        self,
        layer_tree: QgsLayerTreeNode,
        indexFrom: int,  # noqa: N803
        indexTo: int,  # noqa: N803
    ) -> None:
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

            iface.layerTreeView().removeIndicator(layer_tree_node, indicator)


class AttributeShortcutIndicator(QgsLayerTreeViewIndicator):
    """Custom indicator for the attribute shortcut plugin."""

    def __init__(self, layer_id: str) -> None:
        super().__init__()
        self.layer_id = layer_id
        self.setIcon(ATTRIBUTE_TABLE_ICON)
        self.setToolTip(ATTRIBUTE_TABLE_TOOLTIP)
        self.clicked.connect(self.show_attribute_table)

    def show_attribute_table(self) -> None:
        """Show the attribute table for the layer."""
        layers = QgsProject.instance().mapLayers()
        try:
            layer = layers[self.layer_id]
        except KeyError:
            return
        iface.showAttributeTable(layer)
