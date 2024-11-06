from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class GoBackToFilterChoiceButton(QPushButton):
    def __init__(self, dictionary_browser: "DictionaryBrowser"):
        super().__init__("Back", cursor=Qt.CursorShape.PointingHandCursor)
        self.browser = dictionary_browser

        self.hide()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.connect_button(
            lambda: self.browser.layout_manager.switch_to_initial_filter_selection()
        )

    def connect_button(self, callback):
        """Connects the button's clicked signal to the provided callback."""
        self.clicked.connect(callback)

    def resize_go_back_button(self):
        """Repositions the button to the top left corner of the widget."""
        self.setFixedHeight(self.browser.main_widget.height() // 20)
        self.setFixedWidth(self.browser.main_widget.width() // 20)
        font = self.font()
        font.setPointSize(self.browser.main_widget.width() // 100)
        self.setFont(font)
