from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget


class SelectLayoutLabel(QLabel):
    def __init__(self, control_widget: "LayoutControlsWidget"):
        super().__init__("Select Layout:", control_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.control_widget = control_widget

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(max(10, self.control_widget.width() // 50))
        self.setFont(font)
