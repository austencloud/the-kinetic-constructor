from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget
    from .length_selector import LengthSelector

class SequenceLengthLabel(QLabel):
    def __init__(self, length_selector: "LengthSelector"):
        super().__init__("Length:", length_selector)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_selector = length_selector

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(max(10, self.length_selector.layout_tab.width() // 50))
        self.setFont(font)
