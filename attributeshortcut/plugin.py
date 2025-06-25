from __future__ import annotations

from typing import cast

from qgis.core import (
    QgsApplication,
    QgsLayerTree,
    QgsLayerTreeGroup,
    QgsLayerTreeLayer,
    QgsProject,
    QgsVectorLayer,
)
from qgis.gui import (
    QgisInterface,
    QgsLayerTreeView,
    QgsLayerTreeViewIndicator,
)
from qgis.PyQt.QtCore import QCoreApplication, QObject, pyqtSlot
from qgis.utils import iface

iface = cast(QgisInterface, iface)  # Ensure iface is cast to QgsInterface


class Plugin:
    """QGIS Plugin Implementation."""

    name = "attribute-shortcut"

    def __init__(self) -> None:
        self.indicators: list[AttributeShortcutIndicator] = []
        self.connections: list[tuple[QObject, QCoreApplication.pyqtBoundSignal]] = []
        self.object = QObject()

    def initGui(self) -> None:  # noqa N802
        root: QgsLayerTree = QgsProject.instance().layerTreeRoot()
        connection = root.addedChildren.connect(self.add_indicator_to_layers)
        self.connections.append((root, connection))

        self.add_indicator_to_layers(root)

    def unload(self) -> None:
        root = QgsProject.instance().layerTreeRoot()
        root.addedChildren.disconnect(self.add_indicator_to_layers)

        layer_tree_view = iface.layerTreeView()
        for indicator in self.object.findChildren(AttributeShortcutIndicator):
            try:
                layer_tree_view.removeIndicator(indicator.layer_tree_layer, indicator)
            except RuntimeError:
                pass

        self.object.deleteLater()

    def add_indicator_to_layers(self, layer_tree: QgsLayerTreeGroup, *args) -> None:
        """Add a layer tree view indicator to a vector layer."""

        layer_tree_view: QgsLayerTreeView = iface.layerTreeView()

        for layer_tree_layer in layer_tree.findLayers():
            if any(
                isinstance(ind, AttributeShortcutIndicator)
                for ind in layer_tree_view.indicators(layer_tree_layer)
            ):
                continue

            indicator_adder = QgsIndicatorAdder(self.object, layer_tree_layer)

            if not layer_tree_layer.layer():
                layer_tree_layer.layerLoaded.connect(indicator_adder.add_indicator_to_layer)
            else:
                indicator_adder.add_indicator_to_layer()


class QgsIndicatorAdder(QObject):
    """Helper class to add indicators to layer tree layers."""

    def __init__(self, parent: QObject | None, layer_tree_layer: QgsLayerTreeLayer) -> None:
        super().__init__(parent)
        self.layer_tree_layer = layer_tree_layer

    @pyqtSlot()
    def add_indicator_to_layer(
        self,
    ) -> None:
        layer_tree_layer = self.layer_tree_layer

        map_layer = layer_tree_layer.layer()

        if not isinstance(map_layer, QgsVectorLayer):
            return

        indicator = AttributeShortcutIndicator(self.parent(), map_layer, layer_tree_layer)

        iface.layerTreeView().addIndicator(layer_tree_layer, indicator)

        self.deleteLater()


class AttributeShortcutIndicator(QgsLayerTreeViewIndicator):
    """Custom indicator for the attribute shortcut plugin."""

    _icon = QgsApplication.getThemeIcon("mActionOpenTable.svg")

    def __init__(
        self, parent: QObject | None, layer: QgsVectorLayer, layer_tree_layer: QgsLayerTreeLayer
    ) -> None:
        super().__init__(parent)
        self.layer = layer
        self.layer_tree_layer = layer_tree_layer
        self.setIcon(self._icon)
        # Aim to borrow translation from qgis core
        self.setToolTip(
            QgsApplication.translate("QgsMapToolIdentifyAction", "Show Attribute Table")
        )
        self.clicked.connect(lambda: iface.showAttributeTable(layer))
