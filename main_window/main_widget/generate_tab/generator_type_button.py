from PyQt6.QtWidgets import (
    QPushButton,
)
from PyQt6.QtCore import Qt, QEvent
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab



class GeneratorTypeButton(QPushButton):
    def __init__(self, text: str, tab: "GenerateTab", key: str):
        super().__init__(text)
        self.tab = tab
        self.key = key
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def resizeEvent(self, event: QEvent):
        font_size = self.tab.main_widget.width() // 75
        active_style = "background-color: lightblue; font-weight: bold;"
        inactive_style = "background-color: none; font-weight: normal;"
        style = (
            active_style
            if self.tab.current_sequence_generator == self.key
            else inactive_style
        )
        self.setStyleSheet(f"{style} font-size: {font_size}px; padding: 8px;")
        self.setFixedHeight(self.tab.main_widget.height() // 16)
        self.setFixedWidth(self.tab.main_widget.width() // 10)
        super().resizeEvent(event)
