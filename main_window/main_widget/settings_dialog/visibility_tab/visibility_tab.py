from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout

from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab_pictograph import (
    VisibilityTabPictograph,
)

from .visibility_checkbox_widget import VisibilityCheckboxWidget
from .visibility_tab_pictograph_view import VisibilityTabPictographView

if TYPE_CHECKING:
    from ..settings_dialog import SettingsDialog


class VisibilityTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.dialog = settings_dialog
        self.checkbox_widget = VisibilityCheckboxWidget(self)
        self.pictograph = VisibilityTabPictograph(self.main_widget)
        self.pictograph_view = VisibilityTabPictographView(self, self.pictograph)

        layout: QHBoxLayout = QHBoxLayout(self)
        layout.addWidget(self.checkbox_widget)
        layout.addWidget(self.pictograph_view)
        self.setLayout(layout)
