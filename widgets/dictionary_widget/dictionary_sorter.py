from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionarySorter(QWidget):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.setup_ui()

    def setup_ui(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.sort_combobox = QComboBox()
        self.sort_combobox.addItems(["Word Length", "Alphabetical"])
        self.sort_combobox.currentTextChanged.connect(self.on_sort_order_changed)
        self.layout.addWidget(self.sort_combobox)

    def on_sort_order_changed(self, sort_order):
        self.browser.scroll_widget.sort_and_display_thumbnails(sort_order)
