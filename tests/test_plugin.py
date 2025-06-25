"""Tests for the Plugin class."""

import sys
from unittest.mock import Mock, call, patch

import pytest
from qgis.gui import QgsLayerTreeView

from attributeshortcut.plugin import Plugin


class TestPlugin:
    """Test cases for the Plugin class."""

    def test_plugin_initialization(self):
        """Test plugin initialization."""

        Plugin()

    def test_plugin_init_gui(self):
        plugin = Plugin()
        plugin.initGui()
