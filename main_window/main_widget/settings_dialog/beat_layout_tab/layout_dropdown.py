from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget
    from .layout_selector import LayoutSelector


class LayoutDropdown(QComboBox):
    def __init__(self, layout_selector: "LayoutSelector"):
        super().__init__(layout_selector)
        self.layout_selector = layout_selector
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        valid_layout_strs = [
            f"{rows} x {cols}"
            for rows, cols in self.layout_selector.layout_tab.valid_layouts
        ]
        self.addItems(valid_layout_strs)
        self.currentTextChanged.connect(
            lambda layout: self.layout_selector.controls_widget.layout_selected.emit(
                layout
            )
        )

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.layout_selector.layout_tab.width() // 50)
        self.setFont(font)
