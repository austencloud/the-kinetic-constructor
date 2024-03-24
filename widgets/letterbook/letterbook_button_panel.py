from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
from .letterbook_letter_button_frame.letterbook_letter_button_frame import (
    LetterBookLetterButtonFrame,
)

if TYPE_CHECKING:
    from widgets.letterbook.letterbook import LetterBook


class LetterBookButtonPanel(QFrame):
    def __init__(self, letterbook: "LetterBook") -> None:
        super().__init__(letterbook)
        self.letterbook = letterbook
        self.letter_btn_frame = LetterBookLetterButtonFrame(self)
        self._setup_layout()

    def _setup_layout(self) -> QFrame:
        self.setStyleSheet("QFrame { border: 1px solid black; }")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.letter_btn_frame, 30)
