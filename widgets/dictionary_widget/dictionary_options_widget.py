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
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.selected_button: QPushButton = None  # Track the selected button
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
        self.buttons_layout.addStretch(2)
        self.buttons_layout.addWidget(self.sort_by_label)
        self.layout.addLayout(self.buttons_layout)
        self.buttons_layout.addStretch(2)

        for button in self.buttons.values():
            self.buttons_layout.addWidget(button)
            self.buttons_layout.addStretch(1)
        self.buttons_layout.addStretch(2)

    def on_sort_by_length(self):
        self._update_selected_button(self.buttons["sort_by_length_button"])
        self.settings_manager.dictionary.set_sort_method("sequence_length")
        self.browser.sorter.sort_and_display_thumbnails("sequence_length")
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def on_sort_alphabetically(self):
        self._update_selected_button(self.buttons["sort_alphabetically_button"])
        self.settings_manager.dictionary.set_sort_method("alphabetical")
        self.browser.sorter.sort_and_display_thumbnails("alphabetical")
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def on_sort_by_date_added(self):
        self._update_selected_button(self.buttons["sort_date_added_button"])
        self.settings_manager.dictionary.set_sort_method("date_added")
        self.browser.sorter.sort_and_display_thumbnails("date_added")
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def _update_selected_button(self, button: QPushButton):
        if self.selected_button:
            self._style_button(self.selected_button, selected=False)
        self._style_button(button, selected=True)
        self.selected_button = button

    def _style_sort_by_label(self):
        sort_by_label_font = self.sort_by_label.font()
        sort_by_label_font.setPointSize(self.browser.width() // 50)
        self.sort_by_label.setFont(sort_by_label_font)

    def style_buttons(self):
        for button in self.buttons.values():
            selected = button == self.selected_button
            self._style_button(button, selected=selected)

    def _style_button(self, button: QPushButton, selected: bool = False):
        button_font = button.font()
        button_font.setPointSize(self.browser.width() // 65)
        button.setFont(button_font)
        button.setContentsMargins(10, 5, 10, 5)
        font_color = self.settings_manager.global_settings.get_font_color(
            self.settings_manager.global_settings.get_background_type()
        )
        button_background_color = (
            "lightgray" if font_color == "black" else "#555"
        )
        hover_color = "lightgray" if font_color == "black" else "#555"
        if selected:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: {button_background_color};
                    color: {font_color};
                    border-radius: 5px;
                    font-weight: bold;
                    padding: 5px;
                }}
                """
            )
        else:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    background: transparent;
                    border: none;
                    font-weight: bold;
                    color: {font_color};
                    padding: 5px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background: {hover_color};
                }}
                """
            )

    def resizeEvent(self, event):
        self._style_sort_by_label()
        self.style_buttons()
        super().resizeEvent(event)
