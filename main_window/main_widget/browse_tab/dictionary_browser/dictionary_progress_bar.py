from typing import TYPE_CHECKING
from .rainbow_progress_bar import RainbowProgressBar

if TYPE_CHECKING:
    from .dictionary_browser import DictionaryBrowser


class DictionaryProgressBar(RainbowProgressBar):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser.scroll_widget.scroll_content)
        self.browser = browser

    def _style_dictionary_progress_bar(self):
        self.setFixedWidth(self.browser.width() // 3)
        self.setFixedHeight(self.browser.height() // 6)

        font = self.percentage_label.font()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(self.browser.width() // 40)
        self.percentage_label.setFont(font)
        self.loading_label.setFont(font)
