from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import DictionaryBrowser


class SequenceCountLabel(QLabel):
    def __init__(self, dictionary_browser: "DictionaryBrowser"):
        super().__init__("")
        self.browser = dictionary_browser
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_count(self, count: int):
        """Update the label with the count of displayed sequences."""
        self.setText(f"Sequences displayed: {count}")

    def resize_sequence_count_label(self):
        label = self.browser.sequence_count_label
        font = label.font()
        font.setPointSize(self.browser.width() // 80)
        label.setFont(font)
