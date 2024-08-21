from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from widgets.dictionary_widget.dictionary_options_filter_widget import DictionaryOptionsFilterWidget
from widgets.dictionary_widget.dictionary_sort_widget import DictionarySortWidget

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryOptionsWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.sort_widget = DictionarySortWidget(browser)
        self.filter_widget = DictionaryOptionsFilterWidget(browser)

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add the sort widget to the layout
        self.layout.addWidget(self.sort_widget)

        # Add the filter widget to the layout
        self.layout.addWidget(self.filter_widget)
