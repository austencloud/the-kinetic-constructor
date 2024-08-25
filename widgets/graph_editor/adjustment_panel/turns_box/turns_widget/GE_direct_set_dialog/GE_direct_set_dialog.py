from PyQt6.QtWidgets import QDialog, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import BLUE, HEX_BLUE, HEX_RED
from .GE_direct_set_turns_button import GE_DirectSetTurnsButton

if TYPE_CHECKING:
    from ..GE_turns_widget import GE_TurnsWidget
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QFrame


class GE_DirectSetDialog(QDialog):
    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        super().__init__(
            turns_widget, Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup
        )
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.setStyleSheet(
            f"""
            QDialog {{
                border: 2px solid {HEX_BLUE if self.turns_box.color == BLUE else HEX_RED};
                border-radius: 5px;
            }}
        """
        )
        self.buttons: dict[str, GE_DirectSetTurnsButton] = {}

        self._setup_buttons()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        for button in self.buttons.values():
            self.layout.addWidget(button)
        self.adjustSize()

    def _setup_buttons(self):
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]

        for value in turns_values:
            button = GE_DirectSetTurnsButton(value, self.turns_widget)
            button.set_button_styles()
            button.clicked.connect(
                lambda _, v=value: self.select_turns(float(v) if "." in v else int(v))
            )
            self.buttons[value] = button

    def select_turns(self, value):
        self.turns_widget.adjustment_manager.direct_set_turns(value)
        self.accept()

    def resize_direct_set_buttons(self) -> None:
        for button in self.buttons.values():
            button.setMinimumWidth(int(self.turns_widget.width() / 2))
