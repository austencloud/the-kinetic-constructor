from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget


class DefaultLayoutLabel(QLabel):
    def __init__(self, control_widget: "LayoutControlsWidget"):
        super().__init__(
            f"Default: {control_widget.layout_tab.current_layout[0]} x {control_widget.layout_tab.current_layout[1]}",
            control_widget,
        )
        self.control_widget = control_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.font()
        font.setBold(True)
        self.setFont(font)

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.control_widget.width() // 50)
        self.setFont(font)
