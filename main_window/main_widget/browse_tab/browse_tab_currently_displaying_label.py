from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class BrowseTabCurrentlyDisplayingLabel(QLabel):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_message(self, description):
        self.setText(f"Currently displaying {description}.")

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.browser.width() // 65)
        self.setFont(font)
        
