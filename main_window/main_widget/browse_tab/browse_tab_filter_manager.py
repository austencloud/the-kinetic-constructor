from datetime import datetime
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:

    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabFilterManager:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab
        self.main_widget = self.browse_tab.main_widget

    def show_favorites(self):
        """Show only favorite sequences."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("favorite sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        favorites = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if any(
                self.browse_tab.main_widget.metadata_extractor.get_favorite_status(
                    thumbnail
                )
                for thumbnail in thumbnails
            )
        ]

        self.browse_tab.currently_displayed_sequences = favorites
        self.browse_tab.ui_updater.update_and_display_ui(len(favorites))

    def show_all_sequences(self):
        """Show all sequences."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("all sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        sequences = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
        ]

        self.browse_tab.currently_displayed_sequences = sequences
        self.browse_tab.ui_updater.update_and_display_ui(len(sequences))

    def show_most_recent_sequences(self, date: datetime):
        """Show most recent sequences based on date."""
        self.browse_tab.filter_manager.prepare_ui_for_filtering("most recent sequences")
        dictionary_dir = get_images_and_data_path("dictionary")

        most_recent = [
            (
                word,
                thumbnails,
                self.browse_tab.main_widget.metadata_extractor.get_sequence_length(
                    thumbnails[0]
                ),
            )
            for word, thumbnails in self.browse_tab.get.base_words(dictionary_dir)
            if self.browse_tab.section_manager.get_date_added(thumbnails) >= date
        ]

        self.browse_tab.currently_displayed_sequences = most_recent
        self.browse_tab.ui_updater.update_and_display_ui(len(most_recent))

    def show_browser_with_filters_from_settings(self):
        """Show browser with filters from settings."""
        current_filter = (
            self.browse_tab.main_widget.main_window.settings_manager.browse_tab_settings.get_current_filter()
        )

        self.apply_current_filter(current_filter)

    def apply_current_filter(self, current_filter):
        self.current_filter = current_filter
        self.main_widget.fade_manager.fade_to_tab(
            self.main_widget.left_stack,
            self.main_widget.left_sequence_picker_index,
        )

        self.browse_tab.sequence_picker.thumbnail_box_sorter.sort_and_display_thumbnail_boxes_by_current_filter(
            current_filter
        )
        self.browse_tab.sequence_viewer.update_preview(None)
        QApplication.processEvents()

    def prepare_ui_for_filtering(self, description: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.browse_tab.sequence_picker.control_panel.currently_displaying_label.setText(
            ""
        )
        QApplication.processEvents()
        self.browse_tab.sequence_picker.control_panel.currently_displaying_label.show_message(
            description
        )
        self.browse_tab.sequence_picker.control_panel.count_label.setText("")
        self.browse_tab.sequence_picker.scroll_widget.clear_layout()
        self.browse_tab.sequence_picker.scroll_widget.grid_layout.addWidget(
            self.browse_tab.sequence_picker.progress_bar,
            0,
            0,
            1,
            self.browse_tab.sequence_picker.thumbnail_box_sorter.num_columns,
            Qt.AlignmentFlag.AlignCenter,
        )
        self.browse_tab.sequence_picker.progress_bar.setVisible(True)
        self.browse_tab.sequence_picker.progress_bar.resize_progress_bar()

        QApplication.processEvents()
