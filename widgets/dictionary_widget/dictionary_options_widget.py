from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryOptionsWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget

        self._setup_sort_buttons()
        self._setup_layout()

    def _setup_sort_buttons(self):
        self.buttons: dict[str, QPushButton] = {}

        button_data = {
            "sort_by_length_button": {
                "text": "Sequence Length",
                "clicked": self.on_sort_by_length,
            },
            "sort_alphabetically_button": {
                "text": "Alphabetical",
                "clicked": self.on_sort_alphabetically,
            },
            "sort_date_added_button": {
                "text": "Date Added",
                "clicked": self.on_sort_by_date_added,
            },
        }

        for button_name, button_info in button_data.items():
            button = QPushButton(button_info["text"])
            button.clicked.connect(button_info["clicked"])
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[button_name] = button

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.buttons_layout: QHBoxLayout = QHBoxLayout()

        self.sort_by_label = QLabel("Sort:")
        self.sort_by_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.sort_by_label)
        self.layout.addLayout(self.buttons_layout)
        self.buttons_layout.addStretch()

        for button in self.buttons.values():
            self.buttons_layout.addWidget(button)
        self.buttons_layout.addStretch()

    def on_sort_by_length(self):
        self.browser.sorter.sort_and_display_thumbnails("Sequence Length")
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def on_sort_alphabetically(self):
        self.browser.sorter.sort_and_display_thumbnails("Alphabetical")
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def on_sort_by_date_added(self):
        self.browser.sorter.sort_and_display_thumbnails("Date Added")
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def resizeEvent(self, event):
        self._style_sort_by_label()
        self._style_buttons()
        super().resizeEvent(event)

    def _style_sort_by_label(self):
        sort_by_label_font = self.sort_by_label.font()
        sort_by_label_font.setPointSize(self.browser.width() // 50)
        self.sort_by_label.setFont(sort_by_label_font)

    def _style_buttons(self):
        for button in self.buttons.values():
            button_font = button.font()
            button_font.setPointSize(self.browser.width() // 65)
            button.setFont(button_font)
            button.setContentsMargins(10, 5, 10, 5)
            button.setStyleSheet(
                """
                QPushButton {
                    background: transparent;
                    border: none;
                    font-weight: bold;
                    color: #333;
                    padding: 5px;
                    text-align: center;
                }
                QPushButton:hover {
                    background: #f0f0f0;
                }
            """
            )
