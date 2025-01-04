from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QEvent, Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.visibility_tab.visibility_tab import (
        VisibilityTab,
    )


class VisibilityCheckboxWidget(QWidget):
    glyph_checkboxes: dict[str, QCheckBox] = {}
    grid_checkboxes: dict[str, QCheckBox] = {}
    glyph_names = [
        "TKA",
        "VTG",
        "Elemental",
        "Positions",
        "Reversals",
    ]
    grid_names = [
        "Non-radial points",
    ]

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.main_widget = visibility_tab.main_widget
        self.settings = self.main_widget.settings_manager.visibility

        self._create_checkboxes()
        self._setup_layout()
        self.update_checkboxes()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(2)
        for checkbox in list(self.glyph_checkboxes.values()) + list(
            self.grid_checkboxes.values()
        ):
            self.layout.addWidget(checkbox)
            self.layout.addStretch(1)
        self.layout.addStretch(2)

    def _create_checkboxes(self):
        glyph_toggler = self.visibility_tab.settings.glyph_visibility_manager

        for name in self.glyph_names:
            checkbox = QCheckBox(name)
            self.glyph_checkboxes[name] = checkbox
            checkbox.stateChanged.connect(
                lambda state, g=checkbox.text(): glyph_toggler.toggle_glyph_visibility(
                    g, state
                )
            )

        for name in self.grid_names:
            checkbox = QCheckBox(name)
            self.grid_checkboxes[name] = checkbox
            checkbox.stateChanged.connect(
                lambda state, g=checkbox.text(): self.toggle_all_non_radial_points(
                    state
                )
            )

    def toggle_all_non_radial_points(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.settings.set_non_radial_visibility(is_checked)
        self.non_radial_visible = self.settings.get_non_radial_visibility(
            
        )

        pictographs = self.main_widget.pictograph_collector.collect_all_pictographs()
        for pictograph in pictographs:
            pictograph.grid.toggle_non_radial_points(self.non_radial_visible)

    def update_checkboxes(self):
        """Synchronize checkboxes with the current visibility settings."""
        visibility_settings = (
            self.visibility_tab.main_widget.settings_manager.visibility
        )
        for name, checkbox in self.glyph_checkboxes.items():
            checkbox.setChecked(visibility_settings.get_glyph_visibility(name))
        self.grid_checkboxes["Non-radial points"].setChecked(
            visibility_settings.get_non_radial_visibility()
        )

    def resizeEvent(self, event: QEvent):
        width = self.visibility_tab.width()
        font_size = width // 40
        font = QFont()
        font.setPointSize(font_size)
        self._update_font_for_checkboxes(font)
        super().resizeEvent(event)

    def _update_font_for_checkboxes(self, font: QFont):
        for glyph in self.glyph_names:
            self.glyph_checkboxes[glyph].setFont(font)
        for grid in self.grid_names:
            self.grid_checkboxes[grid].setFont(font)
