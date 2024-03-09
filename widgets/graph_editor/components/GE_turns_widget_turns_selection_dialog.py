from PyQt6.QtWidgets import QDialog, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from constants import HEX_BLUE, HEX_RED

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget


class GE_TurnsSelectionDialog(QDialog):
    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        super().__init__(
            turns_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        # add border
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: 5px;
            }}
        """
        )
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        button_size = self.turns_box.width() // 2

        turns_display_font_size = int(
            self.turns_box.turns_panel.graph_editor.width() / 20
        )

        for value in turns_values:
            button = QPushButton(value)
            button.setFixedSize(QSize(button_size, button_size))
            button.setFont(QFont("Arial", turns_display_font_size, QFont.Weight.Bold))
            # Set button style to match the turns display label
            button.setStyleSheet(
                f"""
                QPushButton {{
                    border: 2px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                    border-radius: {button_size // 2}px;
                    background-color: white;
                }}
                QPushButton:hover {{
                    background-color: #f0f0f0;
                }}
            """
            )
            button.clicked.connect(
                lambda _, v=value: self.select_turns(float(v) if "." in v else int(v))
            )
            layout.addWidget(button)

        self.adjustSize()

    def select_turns(self, value):
        self.turns_widget.adjustment_manager.direct_set_turns(value)
        self.accept()
