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

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()
        button_hbox = QHBoxLayout()
        button_hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        available_levels = [1, 2, 3]
        for level in available_levels:
            button = QPushButton(f"Level {level}")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"level_{level}"] = button
            button.clicked.connect(
                lambda checked, l=level: self.initial_selection_widget.on_level_button_clicked(
                    l
                )
            )
            button_hbox.addWidget(button)

        layout.addLayout(button_hbox)
        layout.addStretch(1)

    def display_only_thumbnails_with_level(self, level: str):
        self._prepare_ui_for_filtering(f"level {level} sequences")

        self.browser.currently_displayed_sequences = []
        sequences = self.get_sequences_that_are_a_specific_level(level)
        total_sequences = len(sequences)

        for word, thumbnails in sequences:
            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, self.get_sequence_length_from_thumbnails(thumbnails))
            )

        self._update_and_display_ui(total_sequences, level)

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
