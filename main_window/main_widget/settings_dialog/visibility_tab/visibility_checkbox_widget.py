from functools import partial
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .visibility_tab import VisibilityTab


class VisibilityCheckboxWidget(QWidget):
    glyph_checkboxes: dict[str, QCheckBox] = {}
    non_radial_checkboxes: dict[str, QCheckBox] = {}
    glyph_names = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
    grid_names = ["Non-radial points"]

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.toggler = visibility_tab.toggler

        self._create_checkboxes()
        self._setup_layout()
        self.update_checkboxes()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(4)
        for checkbox in list(self.glyph_checkboxes.values()) + list(
            self.non_radial_checkboxes.values()
        ):
            self.layout.addWidget(checkbox)
            self.layout.addStretch(1)
        self.layout.addStretch(3)

    def _create_checkboxes(self):
        for name in self.glyph_names:
            checkbox = QCheckBox(name)
            self.glyph_checkboxes[name] = checkbox
            checkbox.stateChanged.connect(
                partial(self.toggler.toggle_glyph_visibility, name)
            )

        for name in self.grid_names:
            checkbox = QCheckBox(name)
            self.non_radial_checkboxes[name] = checkbox
            checkbox.stateChanged.connect(self.toggler.toggle_non_radial_points)

    def update_checkboxes(self):
        """Synchronize checkboxes with the current visibility settings."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        for name, checkbox in self.glyph_checkboxes.items():
            checkbox.setChecked(settings.get_glyph_visibility(name))

        non_radial_checkbox = self.non_radial_checkboxes["Non-radial points"]
        non_radial_checkbox.setChecked(settings.get_non_radial_visibility())

    def resizeEvent(self, event: QEvent):
        width = self.visibility_tab.width()
        font_size = width // 40
        font = QFont()
        font.setPointSize(font_size)
        self._update_checkbox_font(font)
        super().resizeEvent(event)

    def _update_checkbox_font(self, font: QFont):
        for glyph in self.glyph_names:
            self.glyph_checkboxes[glyph].setFont(font)
        for grid in self.grid_names:
            self.non_radial_checkboxes[grid].setFont(font)
