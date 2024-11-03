

from typing import TYPE_CHECKING
from main_window.main_widget.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
    RainbowProgressBar,
)
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )
class DictionaryProgressBar(RainbowProgressBar):
    def __init__(self, scroll_content: "QWidget"):
        super().__init__(scroll_content)
        self.scroll_content = scroll_content

    def _style_dictionary_progress_bar(self):
        self.setFixedWidth(self.scroll_content.width() // 3)
        self.setFixedHeight(self.scroll_content.height() // 6)

        font = self.percentage_label.font()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(self.width() // 40)
        self.percentage_label.setFont(font)
        self.loading_label.setFont(font)
