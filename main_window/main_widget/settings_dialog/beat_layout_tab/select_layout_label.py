from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget
    from .layout_selector import LayoutSelector

class SelectLayoutLabel(QLabel):
    def __init__(self, layout_selector: "LayoutSelector"):
        super().__init__("Select Layout:", layout_selector)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_selector = layout_selector

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.layout_selector.layout_tab.width() // 50)
        self.setFont(font)
