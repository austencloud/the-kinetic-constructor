from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.turns_box.turns_box_widgets.turns_widget.turns_widget import (
        TurnsWidget,
    )


class TurnDirectSetManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget

    def setup_direct_set_buttons(self) -> None:
        self.turns_buttons_frame = QFrame()
        self.turns_buttons_layout = QHBoxLayout(self.turns_buttons_frame)
        self.turns_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        for value in turns_values:
            button = QPushButton(value, self.turns_widget)
            button.setMaximumWidth(
                int(self.turns_widget.turns_display_manager.turns_display.width() / 2)
            )
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #c0c0c0;
                    border-radius: 5px;
                    padding: 5px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e5e5e5;
                    border-color: #a0a0a0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """
            )
            button.clicked.connect(
                lambda _, v=value: self.turns_widget.display_manager.set_turns(
                    float(v) if v in ["0.5", "1.5", "2.5"] else int(v)
                )
            )
            self.turns_buttons_layout.addWidget(button)
        self.turns_widget.layout.addWidget(self.turns_buttons_frame)
