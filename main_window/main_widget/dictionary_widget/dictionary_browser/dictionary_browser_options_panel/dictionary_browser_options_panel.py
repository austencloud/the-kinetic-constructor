from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser_options_panel.sort_widget import (
    SortWidget,
)


if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryOptionsPanel(QWidget):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.sort_widget = SortWidget(self)

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.sort_widget)