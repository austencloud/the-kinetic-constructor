from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.beat_layout_tab.layout_selector import (
        LayoutSelector,
    )


class LayoutDropdown(QComboBox):
    def __init__(self, layout_selector: "LayoutSelector"):
        super().__init__(layout_selector)
        self.controls_widget = layout_selector.controls_widget
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        valid_layout_strs = [
            f"{rows} x {cols}"
            for rows, cols in self.controls_widget.layout_tab.valid_layouts
        ]
        self.addItems(valid_layout_strs)
        self.currentTextChanged.connect(
            lambda layout: self.controls_widget.layout_selected.emit(layout)
        )
