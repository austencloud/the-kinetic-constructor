from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from .pictograph.visibility_pictograph import VisibilityPictograph
from .visibility_toggler import VisibilityToggler
from .visibility_checkbox_widget import VisibilityCheckboxWidget
from .pictograph.visibility_pictograph_view import VisibilityPictographView

if TYPE_CHECKING:
    from ..settings_dialog import SettingsDialog


class VisibilityTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.dialog = settings_dialog
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):

        # Managers
        self.toggler = VisibilityToggler(self)

        # Widgets
        self.checkbox_widget = VisibilityCheckboxWidget(self)
        self.pictograph = VisibilityPictograph(self.main_widget)
        self.pictograph_view = VisibilityPictographView(self, self.pictograph)

    def _setup_layout(self):
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.addWidget(self.checkbox_widget)
        layout.addWidget(self.pictograph_view)
        self.setLayout(layout)
