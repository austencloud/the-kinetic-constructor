from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass



class SwapButton(QPushButton):
    def __init__(self) -> None:
        super().__init__()

    def update_attr_box_adjust_turns_button_size(self, button_size) -> None:
        self.button_size = button_size
        self.border_radius = button_size / 2
        self.setMinimumSize(button_size, button_size)
        self.setIconSize(QSize(int(button_size * 0.6), int(button_size * 0.6)))
        self.setStyleSheet(self._get_button_style())
        self.setFont(QFont("Arial", int(button_size * 0.3)))

    def _get_button_style(self):
        return (
            "QPushButton {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(255, 255, 255, 255), "
            "stop:1 rgba(200, 200, 200, 255));"
            "   border-radius: " + str(self.border_radius) + "px;"
            "   border: 1px solid black;"
            "   min-width: " + str(self.button_size) + "px;"
            "   min-height: " + str(self.button_size) + "px;"
            "   max-width: " + str(self.button_size) + "px;"
            "   max-height: " + str(self.button_size) + "px;"
            "}"
            "QPushButton:hover {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(230, 230, 230, 255), "
            "stop:1 rgba(200, 200, 200, 255));"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "stop:0 rgba(204, 228, 247, 255), "
            "stop:1 rgba(164, 209, 247, 255));"
            "}"
        )
