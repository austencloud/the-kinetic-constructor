from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_viewer import (
        SequenceViewer,
    )


class BrowseTabPreviewAreaWordLabel(QLabel):
    def __init__(self, preview_area: "SequenceViewer"):
        super().__init__(preview_area)
        self.preview_area = preview_area
        self.word = ""
        self.setText(self.word)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText(self.word)

    def update_word_label(self, word: str):
        self.word = word
        self.setText(word)

    def resizeEvent(self, event):
        font_size = self.preview_area.width() // 20
        self.setFont(QFont("Georgia", font_size, QFont.Weight.DemiBold))
        while self.fontMetrics().horizontalAdvance(self.word) > self.width():
            font_size -= 1
            self.setFont(QFont("Georgia", font_size, QFont.Weight.DemiBold))
        super().resizeEvent(event)
