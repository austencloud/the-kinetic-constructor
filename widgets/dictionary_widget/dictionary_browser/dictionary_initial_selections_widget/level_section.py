import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication

from widgets.path_helpers.path_helpers import get_images_and_data_path
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class LevelSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Level:")
        self._add_buttons()
        self.browser = self.initial_selection_widget.browser
        self.currently_displaying_label = (
            self.initial_selection_widget.browser.currently_displaying_label
        )
        self.section_manager = self.browser.section_manager
        self.num_columns = self.browser.num_columns
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter
        self.metadata_extractor = self.browser.main_widget.metadata_extractor
        self.main_widget = self.initial_selection_widget.browser.main_widget

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        available_levels = [1, 2, 3]
        for level in available_levels:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(f"Level {level}")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"level_{level}"] = button
            button.clicked.connect(
                lambda checked, l=level: self.initial_selection_widget.on_level_button_clicked(
                    l
                )
            )
            hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)

    ### LEVEL ###

    def display_only_thumbnails_with_level(self, level: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.currently_displaying_label.show_loading_message(f"level {level} sequences")
        self.browser.number_of_currently_displayed_words_label.setText("")
        self.browser.scroll_widget.clear_layout()
        sequences = self.get_sequences_that_are_a_specific_level(level)
        row_index = 0
        column_index = 0
        num_words = 0
        for word, thumbnails in sequences:
            self.thumbnail_box_sorter.add_thumbnail_box(
                row_index, column_index, word, thumbnails
            )
            column_index += 1
            if column_index == self.num_columns:
                column_index = 0
                row_index += 1
            num_words += 1
            # update the num sequence label
            self.browser.number_of_currently_displayed_words_label.setText(
                f"Number of words displayed: {num_words}"
            )
            QApplication.processEvents()
        self.browser.currently_displayed_sequences = [
            (word, thumbnails, self.get_sequence_length_from_thumbnails(thumbnails))
            for word, thumbnails in sequences
        ]

        self.currently_displaying_label.show_completed_message(
            f"level {level} sequences"
        )
        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words displayed: {num_words}"
        )
        QApplication.restoreOverrideCursor()

    def get_sequences_that_are_a_specific_level(self, level: str):
        dictionary_dir = get_images_and_data_path("dictionary")

        base_words = [
            (
                d,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, d)
                ),
                None,
            )
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d)) and "__pycache__" not in d
        ]

        for i, (word, thumbnails, _) in enumerate(base_words):
            sequence_level = self.get_sequence_level_from_thumbnails(thumbnails)

            base_words[i] = (word, thumbnails, sequence_level)

        return [
            (word, thumbnails)
            for word, thumbnails, sequence_level in base_words
            if sequence_level == level
        ]

    def get_sequence_level_from_thumbnails(self, thumbnails):
        for thumbnail in thumbnails:
            level = self.metadata_extractor.get_sequence_level(thumbnail)
            if level:
                return level
        return None

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_sequence_length(thumbnail)
            if length:
                return length
        return None
