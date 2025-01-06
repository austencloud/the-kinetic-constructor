from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QEvent
from .visibility_button import VisibilityButton
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..visibility_tab import VisibilityTab


class VisibilityButtonsWidget(QWidget):
    glyph_checkboxes: dict[str, VisibilityButton] = {}
    non_radial_checkboxes: dict[str, VisibilityButton] = {}
    glyph_names = ["TKA", "Reversals", "VTG", "Elemental", "Positions"]
    grid_names = ["Non-radial points"]

    def __init__(self, visibility_tab: "VisibilityTab"):
        super().__init__()
        self.visibility_tab = visibility_tab
        self.toggler = visibility_tab.toggler

        self._create_buttons()
        self._setup_layout()
        self.update_buttons()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(4)
        for button in {**self.glyph_checkboxes, **self.non_radial_checkboxes}.values():
            self.layout.addWidget(button)
            self.layout.addStretch(1)
        self.layout.addStretch(3)

    def _create_buttons(self):
        for name in self.glyph_names + self.grid_names:
            button = VisibilityButton(name, self)
            if name in self.glyph_names:
                self.glyph_checkboxes[name] = button
            else:
                self.non_radial_checkboxes[name] = button

    def update_buttons(self):
        """Synchronize buttons with the current visibility settings."""
        settings = self.visibility_tab.main_widget.settings_manager.visibility
        for name, button in {
            **self.glyph_checkboxes,
            **self.non_radial_checkboxes,
        }.items():
            if name in self.glyph_names:
                button.is_toggled = settings.get_glyph_visibility(name)
            else:
                button.is_toggled = settings.get_non_radial_visibility()
            button._apply_styles()

    def resizeEvent(self, event: QEvent):
        width = self.visibility_tab.width()
        font_size = width // 40
        font = QFont()
        font.setPointSize(font_size)

        for button in {**self.glyph_checkboxes, **self.non_radial_checkboxes}.values():
            button.setFont(font)

        super().resizeEvent(event)
