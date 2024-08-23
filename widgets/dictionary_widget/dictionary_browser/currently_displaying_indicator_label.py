from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class CurrentlyDisplayingIndicatorLabel(QLabel):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def show_loading_message(self, context: str):
        self.setText(f"Currently displaying {context}. Please wait...")

    def show_completed_message(self, filter_description_prefix, context: str):
        self.setText(f"Currently displaying{filter_description_prefix} {context}.")

    def reset(self):
        self.setText("")
