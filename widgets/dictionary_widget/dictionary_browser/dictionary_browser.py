from typing import TYPE_CHECKING
from widgets.dictionary_widget.dictionary_browser.dictionary_nav_sidebar import (
    DictionaryNavSidebar,
)
from PyQt6.QtCore import QTimer
from widgets.dictionary_widget.dictionary_sorter import DictionarySorter
from .browser_scroll_widget import DictionaryBrowserScrollWidget
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from widgets.dictionary_widget.dictionary_options_widget import DictionaryOptionsWidget

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryBrowser(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        super().__init__(dictionary_widget)
        self.dictionary_widget = dictionary_widget
        self.main_widget = dictionary_widget.main_widget
        self.initialized = False
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        self.nav_sidebar = DictionaryNavSidebar(self)
        self.scroll_widget = DictionaryBrowserScrollWidget(self)
        self.sorter = DictionarySorter(self)
        self.options_widget = DictionaryOptionsWidget(self)

    def showEvent(self, event):
        super().showEvent(event)
        if not self.initialized:
            sort_method = (
                self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
            )
            timer = QTimer(self)
            timer.singleShot(
                500, lambda: self._initialize_and_sort_thumbnails(sort_method)
            )

    def _initialize_and_sort_thumbnails(self, sort_method):
        self.sorter.sort_and_display_thumbnails(sort_method)
        self.initialized = True

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_layout = QHBoxLayout()

        self.layout.addWidget(self.options_widget)
        self.scroll_layout.addWidget(self.nav_sidebar, 1)
        self.scroll_layout.addWidget(self.scroll_widget, 9)

        self.layout.addLayout(self.scroll_layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def resize_dictionary_browser(self):
        self.scroll_widget.resize_dictionary_browser_scroll_widget()

    def display_filtered_sequences(self, filtered_sequences):
        """Display sequences based on the filtered metadata."""
        self.scroll_widget.clear_layout()

        num_columns = 3  # Assuming a grid with 3 columns
        row_index = 0
        column_index = 0

        for metadata_and_thumbnails_dict in filtered_sequences:
            word = metadata_and_thumbnails_dict["metadata"]["sequence"][0]["word"]
            thumbnails = metadata_and_thumbnails_dict["thumbnails"]

            self.sorter._add_thumbnail_box(row_index, column_index, word, thumbnails)

            # Update the row and column index for the grid layout
            column_index += 1
            if column_index == num_columns:
                column_index = 0
                row_index += 1

    def reset_filters(self):
        """Reset filters and display all sequences."""
        self._initialize_and_sort_thumbnails(
            self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )
