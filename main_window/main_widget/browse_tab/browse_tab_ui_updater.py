from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class BrowseTabUIUpdater:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

    def update_and_display_ui(self, total_sequences: int):
        """Update the UI to display the sequences based on filter criteria."""
        if total_sequences == 0:
            total_sequences = 1

        self.browse_tab.sequence_picker.count_label.setText(
            f"Number of words to be displayed: {total_sequences}"
        )

        def update_ui():
            num_words = 0
            for index, (word, thumbnails, _) in enumerate(
                self.browse_tab.currently_displayed_sequences
            ):
                row_index = index // self.browse_tab.thumbnail_box_sorter.num_columns
                column_index = index % self.browse_tab.thumbnail_box_sorter.num_columns
                self.browse_tab.thumbnail_box_sorter.add_thumbnail_box(
                    row_index=row_index,
                    column_index=column_index,
                    word=word,
                    thumbnails=thumbnails,
                    hidden=True,
                )
                num_words += 1

                percentage = int((num_words / total_sequences) * 100)
                self.browse_tab.sequence_picker.progress_bar.set_value(percentage)
                self.browse_tab.sequence_picker.count_label.setText(
                    f"Number of words: {num_words}"
                )
                QApplication.processEvents()

            # Finalize display and update colors
            self.browse_tab.sequence_picker.progress_bar.setVisible(False)
            self._apply_sorting_and_styling()
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)

    def _apply_sorting_and_styling(self):
        """Apply sorting to thumbnails and style elements based on current settings."""
        self.browse_tab.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
            self.browse_tab.main_widget.main_window.settings_manager.browse_tab_settings.get_sort_method()
        )

        font_color = self.browse_tab.main_widget.font_color_updater.get_font_color(
            self.browse_tab.main_widget.main_window.settings_manager.global_settings.get_background_type()
        )

        # Update style for each thumbnail box
        for (
            thumbnail_box
        ) in self.browse_tab.sequence_picker.scroll_widget.thumbnail_boxes.values():
            thumbnail_box.word_label.setStyleSheet(f"color: {font_color};")
            thumbnail_box.word_label.star_icon_empty_path = (
                "star_empty_white.png"
                if font_color == "white"
                else "star_empty_black.png"
            )
            thumbnail_box.word_label.reload_favorite_icon()
            thumbnail_box.variation_number_label.setStyleSheet(f"color: {font_color};")
