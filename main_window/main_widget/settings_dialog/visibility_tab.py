from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QCheckBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog

class VisibilityTab(QWidget):
    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__()
        self.main_widget = settings_dialog.main_widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Visibility Settings")
        title.setFont(self._get_title_font())
        layout.addWidget(title)

        # Glyph visibility settings
        glyph_visibility_manager = (
            self.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]

        for glyph in glyph_types:
            checkbox = QCheckBox(glyph)
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))
            checkbox.setFont(self._get_default_font())
            checkbox.stateChanged.connect(
                lambda state, g=glyph: self._toggle_glyph_visibility(g, state)
            )
            layout.addWidget(checkbox)

        # Non-radial points visibility
        grid_visibility_manager = (
            self.main_widget.settings_manager.visibility.grid_visibility_manager
        )
        non_radial_checkbox = QCheckBox("Non-Radial Points")
        non_radial_checkbox.setChecked(grid_visibility_manager.non_radial_visible)
        non_radial_checkbox.setFont(self._get_default_font())
        non_radial_checkbox.stateChanged.connect(
            lambda state: self._toggle_non_radial_visibility(state)
        )
        layout.addWidget(non_radial_checkbox)

        layout.addSpacerItem(
            QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )
        self.setLayout(layout)

    def _toggle_glyph_visibility(self, glyph: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.main_widget.settings_manager.visibility.set_glyph_visibility(
            glyph, is_checked
        )

    def _toggle_non_radial_visibility(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        grid_visibility_manager = (
            self.main_widget.settings_manager.visibility.grid_visibility_manager
        )
        grid_visibility_manager.set_non_radial_visibility(is_checked)

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font
