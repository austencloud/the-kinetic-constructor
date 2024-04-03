from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QFrame
from PyQt6.QtCore import Qt
from .codex_letter_button_frame.codex_letter_button_frame import CodexLetterButtonFrame

if TYPE_CHECKING:
    from widgets.codex.codex import Codex


class CodexButtonPanel(QFrame):
    def __init__(self, codex: "Codex") -> None:
        super().__init__(codex)
        self.codex = codex
        self.letter_btn_frame = CodexLetterButtonFrame(self)
        self._setup_layout()

    def _setup_layout(self) -> QFrame:
        self.setStyleSheet("QFrame { border: 1px solid black; }")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.letter_btn_frame, 30)
