from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Callable

from widgets.factories.button_factory.buttons.letterbook_adjust_turns_button import (
    LetterBookAdjustTurnsButton,
)
from widgets.factories.button_factory.buttons.swap_button import SwapButton

if TYPE_CHECKING:
    from widgets.letterbook.letterbook_letter_button_frame.components.letterbook_turns_box import (
        LetterBookTurnsBox,
    )


class GE_TurnsBoxWidget(QWidget):
    def __init__(self, turns_box) -> None:
        super().__init__(turns_box)
        self.turns_box: "LetterBookTurnsBox" = turns_box

    def create_attr_header_label(
        self, text: str, align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter
    ) -> QLabel:
        attr_label = QLabel(text, self)
        attr_label.setFont(QFont("Arial"))
        attr_label.setAlignment(align)
        attr_label.setContentsMargins(0, 0, 0, 0)
        return attr_label

    def create_header_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_swap_button(self, icon_path: str, callback: Callable) -> "SwapButton":
        button = SwapButton(self.turns_box, icon_path)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def create_adjust_turns_button(self, text: str) -> LetterBookAdjustTurnsButton:
        button = LetterBookAdjustTurnsButton(self)
        button.setText(text)
        return button
