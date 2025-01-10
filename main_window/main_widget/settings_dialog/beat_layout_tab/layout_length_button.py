from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget


class LayoutLengthButton(QPushButton):
    def __init__(
        self, text: str, control_widget: "LayoutControlsWidget", callback: callable
    ):
        super().__init__(text, control_widget)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(callback)
        self.control_widget = control_widget

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(max(10, self.control_widget.width() // 50))
        self.setFont(font)
