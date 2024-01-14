from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from widgets.attr_box_widgets.turns_widgets.base_turns_widget.base_turns_widget import (
        BaseTurnsWidget,
    )


class DirectSetTurnsManager:
    def __init__(self, parent_widget: "BaseTurnsWidget") -> None:
        self.parent_widget = parent_widget

    def setup_direct_set_buttons(self):
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.parent_widget.turns_buttons_layout = QHBoxLayout()

        for value in turns_values:
            button = self.create_button(value)
            self.parent_widget.turns_buttons_layout.addWidget(button)

    def create_button(self, value: str) -> QPushButton:
        button = QPushButton(value, self.parent_widget)
        button.setStyleSheet(self._get_direct_set_button_style_sheet())
        button.setContentsMargins(0, 0, 0, 0)
        button.setMinimumWidth(button.fontMetrics().boundingRect(value).width() + 10)
        button.clicked.connect(lambda _, v=value: self._directly_set_turns(float(v)))
        return button

    def _directly_set_turns(self, new_turns: Union[int, float]) -> None:
        new_turns = int(new_turns) if new_turns.is_integer() else new_turns
        self.parent_widget.update_turns_display(new_turns)
        self.parent_widget.set_turns(new_turns)

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
