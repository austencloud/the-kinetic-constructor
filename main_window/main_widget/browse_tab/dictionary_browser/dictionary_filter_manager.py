from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryFilterManager:
    def __init__(self, browser: "DictionaryBrowser"):
        self.browser = browser

    def show_favorites(self):
        """Show only favorite sequences."""
        self.browser.filter_manager.prepare_ui_for_filtering("favorite sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        favorites = [
            (
                word,
                thumbnails,
                self.browser.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browser.get.base_words(dictionary_dir)
            if any(
                self.browser.main_widget.metadata_extractor.get_favorite_status(
                    thumbnail
                )
                for thumbnail in thumbnails
            )
        ]

        self.browser.currently_displayed_sequences = favorites
        self.browser.ui_updater.update_and_display_ui(
            len(favorites), "favorite sequences"
        )

    def show_all_sequences(self):
        """Show all sequences."""
        self.browser.filter_manager.prepare_ui_for_filtering("all sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        sequences = [
            (
                word,
                thumbnails,
                self.browser.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browser.get.base_words(dictionary_dir)
        ]

        self.browser.currently_displayed_sequences = sequences
        self.browser.ui_updater.update_and_display_ui(len(sequences), "all sequences")

    def show_most_recent_sequences(self, date: datetime):
        """Show most recent sequences based on date."""
        self.browser.filter_manager.prepare_ui_for_filtering("most recent sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        most_recent = [
            (
                word,
                thumbnails,
                self.browser.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browser.get.base_words(dictionary_dir)
            if self.browser.section_manager.get_date_added(thumbnails) >= date
        ]

        self.browser.currently_displayed_sequences = most_recent
        self.browser.ui_updater.update_and_display_ui(
            len(most_recent), "most recent sequences"
        )

    def show_browser_with_filters_from_settings(self):
        """Show browser with filters from settings."""
        current_filter = (
            self.browser.main_widget.main_window.settings_manager.dictionary_settings.get_current_filter()
        )

        self.apply_current_filter(current_filter)

    def apply_current_filter(self, current_filter):
        self.current_filter = current_filter
        self.browser.layout_manager.switch_to_main_content()
        self.browser.thumbnail_box_sorter.sort_and_display_thumbnail_boxes_by_current_filter(
            current_filter
        )
        self.browser.browse_tab.preview_area.update_preview(None)
        QApplication.processEvents()

    def prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.browser.currently_displaying_label.setText("")
        QApplication.processEvents()
        self.browser.currently_displaying_label.show_message(description)
        self.browser.sequence_count_label.setText("")
        self.browser.scroll_widget.clear_layout()
        self.browser.scroll_widget.grid_layout.addWidget(
            self.browser.progress_bar,
            0,
            0,
            1,
            self.browser.thumbnail_box_sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.browser.progress_bar._style_dictionary_progress_bar()
        self.browser.progress_bar.setVisible(True)
        QApplication.processEvents()
