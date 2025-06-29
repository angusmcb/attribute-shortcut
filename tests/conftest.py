"""
This class contains fixtures and common helper function to keep the test files
shorter.

pytest-qgis (https://pypi.org/project/pytest-qgis) contains the following helpful
fixtures:

* qgis_app initializes and returns fully configured QgsApplication.
  This fixture is called automatically on the start of pytest session.
* qgis_canvas initializes and returns QgsMapCanvas
* qgis_iface returns mocked QgsInterface
* new_project makes sure that all the map layers and configurations are removed.
  This should be used with tests that add stuff to QgsProject.

"""

from unittest.mock import Mock

import pytest
from qgis.gui import QgsLayerTreeView, QgsMessageBar


@pytest.fixture(autouse=True, scope="session")
def patch_iface(qgis_app, qgis_iface):
    qgis_iface.statusBarIface = Mock()
    layer_tree_view = QgsLayerTreeView()
    qgis_iface.layerTreeView = lambda: layer_tree_view
    qgis_iface.addToolBarWidget = Mock()
    message_bar = QgsMessageBar()
    qgis_iface.messageBar = lambda: message_bar
