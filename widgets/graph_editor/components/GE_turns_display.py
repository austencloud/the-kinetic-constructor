from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from data.constants import BLUE, RED

if TYPE_CHECKING:
    from widgets.graph_editor.components.turns_box.turns_widget.GE_turns_widget import (
        GE_TurnsWidget,
    )


class GE_TurnsDisplay(QLabel):
    clicked = pyqtSignal()

    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        super().__init__()
        self.turns_box = turns_widget.turns_box
        self.turns_display_font_size = 20
        self.set_turn_display_styles()

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.clicked.emit()

    def enterEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.set_turn_display_styles(mouse_over=True)

    def leaveEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.set_turn_display_styles()

    def set_turn_display_styles(self, mouse_over=False) -> None:
        self.turns_display_font_size = int(
            (self.turns_box.adjustment_panel.graph_editor.width() / 20)
        )
        self.setFont(QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold))
        self.setFixedSize(
            int(self.turns_box.adjustment_panel.width() / 6),
            int(self.turns_box.adjustment_panel.height() / 4),
        )
        border_radius = self.width() // 4

        turn_display_border = int(self.width() / 20)

        turns_box_color = self.turns_box.color
        if turns_box_color == RED:
            border_color = "#ED1C24"
        elif turns_box_color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"

        self.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid {border_color};
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )
