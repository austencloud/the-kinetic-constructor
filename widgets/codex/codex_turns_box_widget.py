from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Callable

from widgets.factories.button_factory.buttons.swap_button import SwapButton
from ..factories.button_factory.buttons.adjust_turns_button import AdjustTurnsButton

if TYPE_CHECKING:
    from widgets.turns_box.codex_turns_box import CodexTurnsBox


class CodexWidget(QWidget):
    def __init__(self, turns_box) -> None:
        super().__init__(turns_box)
        self.turns_box: "CodexTurnsBox" = turns_box

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

