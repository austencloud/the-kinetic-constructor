from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.settings_dialog.beat_layout_tab.layout_dropdown import LayoutDropdown
from main_window.main_widget.settings_dialog.beat_layout_tab.select_layout_label import (
    SelectLayoutLabel,
)

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget




class LayoutSelector(QFrame):
    def __init__(self, controls_widget: "LayoutControlsWidget"):
        super().__init__(controls_widget)
        self.controls_widget = controls_widget

        self.layout_dropdown_label = SelectLayoutLabel(self)
        self.layout_dropdown = LayoutDropdown(self)

        self._setup_layout()

    def _setup_layout(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)

        layout.addWidget(self.layout_dropdown_label)
        layout.addWidget(self.layout_dropdown)
