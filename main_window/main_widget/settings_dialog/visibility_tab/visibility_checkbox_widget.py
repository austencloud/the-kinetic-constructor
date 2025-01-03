from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )


class VisibilityCheckboxWidget(QWidget):
    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.glyph_checkboxes: dict[str, QCheckBox] = {}
        self.grid_checkboxes: dict[str, QCheckBox] = {}
        self._setup_ui()

    def _setup_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(2)
        self.glyph_names = [
            "TKA",
            "VTG",
            "Elemental",
            "Positions",
            "Reversals",
        ]
        self.grid_names = [
            "Non-radial points",
        ]
        self._create_checkboxes()
        for checkbox in self.glyph_checkboxes.values():
            name = checkbox.text()
            checkbox.stateChanged.connect(
                lambda state, g=name: self._toggle_glyph_visibility(g, state)
            )
        for checkbox in self.grid_checkboxes.values():
            name = checkbox.text()
            checkbox.stateChanged.connect(
                lambda state, g=name: self._toggle_grid_visibility(state)
            )
        self.layout.addStretch(2)

        self.update_checkboxes()

    def _create_checkboxes(self):
        glyph_visibility_manager = (
            self.visibility_tab.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        for name in self.glyph_names + self.grid_names:
            checkbox = QCheckBox(name)
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(name))
            self.layout.addWidget(checkbox)
            self.layout.addStretch(1)
            if name in self.grid_names:
                self.grid_checkboxes[name] = checkbox
            else:
                self.glyph_checkboxes[name] = checkbox

    def _toggle_grid_visibility(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.visibility_tab.settings.set_grid_visibility(
            "non_radial_points", is_checked
        )

    def _toggle_glyph_visibility(self, name: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.visibility_tab.settings.set_glyph_visibility(name, is_checked)

    def update_checkboxes(self):
        """Synchronize checkboxes with the current visibility settings."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        for name, checkbox in self.glyph_checkboxes.items():
            checkbox.setChecked(settings.get_glyph_visibility(name))
        for name, checkbox in self.grid_checkboxes.items():
            checkbox.setChecked(settings.get_grid_visibility(name))

    def resizeEvent(self, event: QEvent):
        width = self.visibility_tab.width()
        font_size = width // 40
        font = QFont()
        font.setPointSize(font_size)
        for glyph in self.glyph_names:
            self.glyph_checkboxes[glyph].setFont(font)
        for grid in self.grid_names:
            self.grid_checkboxes[grid].setFont(font)
        super().resizeEvent(event)
