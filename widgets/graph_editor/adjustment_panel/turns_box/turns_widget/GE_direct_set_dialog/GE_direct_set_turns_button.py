from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from data.constants import BLUE, HEX_BLUE, HEX_RED

if TYPE_CHECKING:
    from widgets.graph_editor.adjustment_panel.turns_box.turns_widget.GE_direct_set_dialog.GE_direct_set_dialog import GE_DirectSetDialog
    from widgets.graph_editor.adjustment_panel.turns_box.turns_widget.GE_turns_widget import (
        GE_TurnsWidget,
    )


class GE_DirectSetTurnsButton(QPushButton):
    def __init__(self, value, direct_set_dialog: "GE_DirectSetDialog") -> None:
        super().__init__(value)
        self.turns_widget = direct_set_dialog.turns_widget
        self.turns_box = self.turns_widget.turns_box
        self.clicked.connect(self.direct_set_adjustment)
        self.setMouseTracking(True)
        
    def enterEvent(self, event) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.PointingHandCursor)

    def leaveEvent(self, event) -> None:
        QApplication.restoreOverrideCursor()

    def direct_set_adjustment(self):
        print("Direct set adjustment button clicked!")

    def set_button_styles(self) -> None:
        button_size = self.turns_box.width() // 2
        turns_display_font_size = int(
            self.turns_box.adjustment_panel.graph_editor.width() / 20
        )
        self.setFixedSize(QSize(button_size, button_size))
        self.setFont(QFont("Arial", turns_display_font_size, QFont.Weight.Bold))
        self.setStyleSheet(
            f"""
            QPushButton {{
                border: 4px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: {button_size // 2}px;
                background-color: white;
            }}
            QPushButton:hover {{
                background-color: #f0f0f0;
            }}
        """
        )

    def resize_direct_set_turns_button(self) -> None:
        self.setFixedSize(
            int(self.turns_widget.width() / 2), int(self.turns_widget.width() / 2)
        )
