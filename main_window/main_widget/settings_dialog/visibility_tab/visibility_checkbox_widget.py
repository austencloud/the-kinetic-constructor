from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import VisibilityTab


class VisibilityCheckboxWidget(QWidget):
    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.glyph_checkboxes: dict[str, QCheckBox] = {}
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self._setup_ui()

    def _setup_ui(self):
        header = QLabel("Visibility Settings")
        header.setFont(self._get_title_font())
        self.layout.addWidget(header)

        glyph_visibility_manager = (
            self.visibility_tab.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]

        for glyph in glyph_types:
            checkbox = QCheckBox(glyph)
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))
            checkbox.setFont(self._get_default_font())
            checkbox.stateChanged.connect(
                lambda state, g=glyph: self._toggle_glyph_visibility(g, state)
            )
            self.layout.addWidget(checkbox)
            self.glyph_checkboxes[glyph] = checkbox

        spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.layout.addItem(spacer)

    def _toggle_glyph_visibility(self, glyph: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.visibility_tab.settings.set_glyph_visibility(glyph, is_checked)
        self.visibility_tab.pictograph_view.update_visibility_from_settings()

    def update_checkboxes(self):
        """Synchronize checkboxes with the current visibility settings."""
        glyph_visibility_manager = (
            self.visibility_tab.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        for glyph, checkbox in self.glyph_checkboxes.items():
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))

    def _get_title_font(self):
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        return font

    def _get_default_font(self):
        font = QFont()
        font.setPointSize(12)
        return font
