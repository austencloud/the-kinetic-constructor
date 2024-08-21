from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)

from widgets.sequence_widget.SW_beat_frame.current_word_line_edit import (
    CurrentWordLineEdit,
)
from word_simplifier import WordSimplifier

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget



class CurrentWordLabel(QWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.current_word = None
        self.line_edit = CurrentWordLineEdit(self)
        layout = QHBoxLayout()
        layout.addWidget(self.line_edit)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

    def resize_current_word_label(self):
        sequence_widget_width = self.sequence_widget.width()
        self.font_size = sequence_widget_width // 30
        font = QFont()
        font.setPointSize(int(self.font_size))
        self.line_edit.setFont(font)
        self.line_edit.kerning = int(self.font_size // 8.75)

    def set_current_word(self, word: str):
        simplified_word = WordSimplifier.simplify_repeated_word(word)
        self.current_word = simplified_word
        self.line_edit.setText(simplified_word)

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
