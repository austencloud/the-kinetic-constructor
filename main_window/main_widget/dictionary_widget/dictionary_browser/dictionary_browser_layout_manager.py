from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedLayout, QHBoxLayout

if TYPE_CHECKING:
    from .dictionary_browser import DictionaryBrowser


class DictionaryBrowserLayoutManager:
    def __init__(self, browser: "DictionaryBrowser"):
        self.browser = browser
        self.layout = QVBoxLayout(self.browser)
        self.stacked_layout = QStackedLayout()

        # Define the main content widget to hold scroll widget and preview area
        self.main_content_widget = QWidget()

    def setup_layout(self):
        """Sets up the main layout structure using QStackedLayout."""
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.browser.setContentsMargins(0, 0, 0, 0)

        initial_layout = QVBoxLayout()
        initial_layout.addWidget(self.browser.initial_selection_widget)

        self.main_content_layout = QVBoxLayout(self.main_content_widget)
        self.main_content_layout.addWidget(self.browser.go_back_button)
        self.main_content_layout.addWidget(self.browser.currently_displaying_label)
        self.main_content_layout.addWidget(self.browser.sequence_count_label)
        self.main_content_layout.addWidget(self.browser.options_widget)

        self.scroll_widget_container = QWidget()
        self.scroll_layout = QHBoxLayout(self.scroll_widget_container)
        self.scroll_layout.addWidget(self.browser.nav_sidebar, 1)
        self.scroll_layout.addWidget(self.browser.scroll_widget, 9)
        self.main_content_layout.addWidget(self.scroll_widget_container)

        self.stacked_layout.addWidget(self.browser.initial_selection_widget)  # Page 0
        self.stacked_layout.addWidget(self.main_content_widget)  # Page 1
        self.layout.addLayout(self.stacked_layout)
        self.stacked_layout.setCurrentIndex(0)  # Show initial page by default

    def switch_to_main_content(self):
        """Switch to the main content page in the stacked layout."""
        self.browser.go_back_button.show()
        self.browser.dictionary.preview_area.show()
        self.stacked_layout.setCurrentIndex(1)
        self.browser.resize_dictionary_browser()

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        self.stacked_layout.setCurrentIndex(0)

        self.browser.initial_selection_widget.show()
        self.browser.dictionary.preview_area.hide()
        self.browser.sequence_count_label.hide()
        self.browser.dictionary.dictionary_settings.set_current_section("filter_choice")
        self.browser.dictionary.dictionary_settings.set_current_filter(None)
        self.browser.initial_selection_widget.show_section("filter_choice")
