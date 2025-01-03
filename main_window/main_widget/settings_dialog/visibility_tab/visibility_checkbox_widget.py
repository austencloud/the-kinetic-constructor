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
        self._setup_ui()

    def _setup_ui(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch(2)
        glyph_visibility_manager = (
            self.visibility_tab.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        self.glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]

        for glyph in self.glyph_types:
            checkbox = QCheckBox(glyph)
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))
            checkbox.stateChanged.connect(
                lambda state, g=glyph: self._toggle_glyph_visibility(g, state)
            )
            self.layout.addWidget(checkbox)
            self.layout.addStretch(1)
            self.glyph_checkboxes[glyph] = checkbox
        self.layout.addStretch(1)


    def _toggle_glyph_visibility(self, glyph: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.visibility_tab.settings.set_glyph_visibility(glyph, is_checked)

    def update_checkboxes(self):
        """Synchronize checkboxes with the current visibility settings."""
        glyph_visibility_manager = (
            self.visibility_tab.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        for glyph, checkbox in self.glyph_checkboxes.items():
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))

    def resizeEvent(self, event: QEvent):
        width = self.visibility_tab.width()
        font_size = width // 40
        font = QFont()
        font.setPointSize(font_size)
        for glyph in self.glyph_types:
            self.glyph_checkboxes[glyph].setFont(font)
        super().resizeEvent(event)
