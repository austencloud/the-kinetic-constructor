from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)


from ..beat_frame.current_word_line_edit import CurrentWordLineEdit
from utilities.word_simplifier import WordSimplifier

if TYPE_CHECKING:
    from ..sequence_widget import SequenceWorkbench

WORD_LENGTH = 8


class CurrentWordLabel(QWidget):
    def __init__(self, sequence_widget: "SequenceWorkbench"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.current_word = None
        self.line_edit = CurrentWordLineEdit(self)
        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = self.sequence_widget.main_widget.width() // 60
        self.font: QFont = QFont()
        self.font.setPointSize(int(font_size))
        self.line_edit.setFont(self.font)
        self.line_edit.kerning = int(font_size // 8.75)

    def set_current_word(self, word: str):
        self.simplified_word = WordSimplifier.simplify_repeated_word(word)
        self.current_word = self.simplified_word

        # Get the first 8 letter characters of the word, including the dash
        count = 0
        result = []
        for char in self.simplified_word:
            if char.isalpha():
                count += 1
            result.append(char)
            if count == WORD_LENGTH:
                break

        # Join the result list to form the final string
        truncated_word = "".join(result)

        # Add "..." if the count is higher than WORD_LENGTH
        word_without_dashes = self.simplified_word.replace("-", "")
        truncated_word_without_dashes = truncated_word.replace("-", "")

        if count == WORD_LENGTH and len(word_without_dashes) > len(
            truncated_word_without_dashes
        ):
            truncated_word += "..."

        self.line_edit.setText(truncated_word)
        self.resizeEvent(None)

    def set_font_color(self, color: str):
        self.line_edit.setStyleSheet(
            f"""
            QLineEdit {{
                background-color: transparent;
                border: none;
                padding-top: 0px;
                padding-bottom: 0px;
                margin: 0px;
                line-height: 1.0em;
                font-family: Georgia;
                font-weight: 600;
                color: {color};
            }}
            """
        )

    def update_current_word_label_from_beats(self):
        current_word = self.sequence_widget.beat_frame.get.current_word()
        self.set_current_word(current_word)
