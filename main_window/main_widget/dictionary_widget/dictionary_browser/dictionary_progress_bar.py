
from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
    DictionaryBrowser,
)
from main_window.main_widget.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
    RainbowProgressBar,
)


class DictionaryProgressBar(RainbowProgressBar):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser)
        self.browser = browser

    def _style_dictionary_progress_bar(self):
        self.setFixedWidth(self.browser.width() // 3)
        self.setFixedHeight(self.browser.height() // 6)

        font = self.percentage_label.font()
        font.setFamily("Monotype Corsiva")
        font.setPointSize(self.width() // 40)
        self.percentage_label.setFont(font)
        self.loading_label.setFont(font)
