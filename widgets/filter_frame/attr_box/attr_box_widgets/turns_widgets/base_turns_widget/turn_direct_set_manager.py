from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QFrame
from typing import TYPE_CHECKING, Union
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from .base_turns_widget import BaseTurnsWidget


class TurnDirectSetManager:
    def __init__(self, parent_widget: "BaseTurnsWidget") -> None:
        self.parent_widget = parent_widget

    def setup_direct_set_buttons(self) -> None:
        self.turns_buttons_frame = QFrame()
        self.turns_buttons_layout = QHBoxLayout(self.turns_buttons_frame)
        self.turns_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.turns_buttons_layout.setSpacing(0)
        self.turns_buttons_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter,
        )
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]

        for value in turns_values:
            button = self.create_button(value)
            self.turns_buttons_layout.addWidget(button)
        self.add_direct_set_turns_to_vbox_layout()

    def create_button(self, value: str) -> QPushButton:
        button = QPushButton(value, self.parent_widget)
        button.setStyleSheet(self._get_direct_set_button_style_sheet())
        button.setContentsMargins(0, 0, 0, 0)
        button.clicked.connect(
            lambda _, v=value: self._directly_set_turns(
                float(v) if v in ["0.5", "1.5", "2.5"] else int(v)
            )
        )
        button.setMaximumWidth(
            int(self.parent_widget.turn_display_manager.turns_display.width() / 2)
        )
        return button

    def _directly_set_turns(self, new_turns: Union[int, float]) -> None:
        self.parent_widget.turn_adjustment_manager.set_turns(new_turns)

    @staticmethod
    def _get_direct_set_button_style_sheet() -> str:
        """Get the style sheet for the direct set turns buttons."""
        return """
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

    def add_direct_set_turns_to_vbox_layout(self) -> None:
        self.parent_widget.vbox_layout.addWidget(self.turns_buttons_frame)
