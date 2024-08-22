import os
from datetime import datetime
from typing import TYPE_CHECKING
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
from widgets.path_helpers.path_helpers import get_images_and_data_path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class ThumbnailBoxSorter:
    def __init__(self, browser: "DictionaryBrowser") -> None:
        self.browser = browser
        self.metadata_extractor = browser.main_widget.metadata_extractor
        self.main_widget = browser.main_widget
        self.section_manager = browser.section_manager

    def sort_and_display_all_thumbnail_boxes_by_sort_method(
        self, sort_method: str
    ) -> None:
        self.browser.currently_displaying_indicator_label.setText(
            f"Currently displaying all sequences. Please wait, this will take a moment..."
        )
        self.browser.options_widget.sort_widget.highlight_appropriate_button(
            sort_method
        )
        self.browser.scroll_widget.clear_layout()
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}

        base_words = self._get_sorted_base_words(sort_method)
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3
        num_sequences = 0
        for word, thumbnails, seq_length in base_words:
            section = self.section_manager.get_section_from_word(
                word, sort_method, seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))
        sorted_sections = self.section_manager.get_sorted_sections(
            sort_method, self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, sort_method)
        QApplication.processEvents()
        for section in sorted_sections:
            if sort_method == "date_added":
                if section == "Unknown":
                    continue

                day, month, year = section.split("-")
                formatted_day = f"{int(day)}-{int(month)}"

                if year != current_section:
                    row_index += 1
                    self.section_manager.add_header(row_index, num_columns, year)
                    row_index += 1
                    current_section = year

                row_index += 1
                self.section_manager.add_header(row_index, num_columns, formatted_day)
                row_index += 1
            else:
                row_index += 1
                self.section_manager.add_header(row_index, num_columns, section)
                row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == num_columns:
                    column_index = 0
                    row_index += 1
        self.browser.currently_displaying_indicator_label.setText(
            f"Currently displaying all sequences."
        )
        # update the number of currently displayed sequences in the label
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {len(base_words)}"
        )

    def sort_and_display_thumbnail_boxes_by_initial_selection(
        self, initial_selection: dict
    ):
        if "letter" in initial_selection.keys():
            if initial_selection["letter"] == "Show all":
                self.sort_and_display_all_thumbnail_boxes_by_sort_method(
                    self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
                )
            else:
                self.display_only_thumbnails_starting_with_letter(
                    initial_selection["letter"]
                )
        elif "length" in initial_selection.keys():
            self.display_only_thumbnails_with_sequence_length(
                initial_selection["length"]
            )
        elif "level" in initial_selection.keys():
            self.display_only_thumbnails_with_level(initial_selection["level"])
        elif "contains_letters" in initial_selection.keys():
            self.display_only_thumbnails_containing_letters(
                initial_selection["contains_letters"]
            )

    def display_only_thumbnails_containing_letters(self, letters: set[str]):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        letters_string = ", ".join(letters)
        if len(letters) == 1:
            self.browser.currently_displaying_indicator_label.setText(
                f"Currently displaying sequences containing {letters_string}. Please wait..."
            )
        elif len(letters) > 1:
            self.browser.currently_displaying_indicator_label.setText(
                f"Currently displaying sequences containing any of: {letters_string}. Please wait..."
            )

        self.browser.number_of_currently_displayed_sequences_label.setText("")
    
        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        base_words = self._get_sorted_base_words("sequence_length")
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3
        num_sequences = 0

        for word, thumbnails, seq_length in base_words:
            # Check if any of the selected letters are in the word
            if not any(letter in word for letter in letters):
                continue

            section = self.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))
            num_sequences += 1
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")
        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == num_columns:
                    column_index = 0
                    row_index += 1

        if len(letters) == 1:
            self.browser.currently_displaying_indicator_label.setText(
                f"Currently displaying sequences containing {letters_string}."
            )
        elif len(letters) > 1:
            self.browser.currently_displaying_indicator_label.setText(
                f"Currently displaying sequences containing any of: {letters_string}."
            )
        # update the number of currently displayed sequences in the label
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    def display_only_thumbnails_with_sequence_length(self, length: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.browser.currently_displaying_indicator_label.setText(
            f"Currently displaying sequences of length {length}. Please wait..."
        )
        self.browser.number_of_currently_displayed_sequences_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        base_words = self._get_sorted_base_words("sequence_length")
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3
        num_sequences = 0
        for word, thumbnails, seq_length in base_words:
            if seq_length != length:
                continue

            section = self.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))
            num_sequences += 1
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")
        QApplication.processEvents()
        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == num_columns:
                    column_index = 0
                    row_index += 1
        self.browser.currently_displaying_indicator_label.setText(
            f"Currently displaying sequences of length {length}"
        )
        # update the number of currently displayed sequences in the label
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    def display_only_thumbnails_with_level(self, level: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        num_sequences = 0

        self.browser.currently_displaying_indicator_label.setText(
            f"Currently displaying level {level} sequences. Please wait..."
        )

        self.browser.number_of_currently_displayed_sequences_label.setText("")
        self.browser.scroll_widget.clear_layout()
        sequences = self.get_sequences_that_are_a_specific_level(level)
        num_columns = 3
        row_index = 0
        column_index = 0
        num_sequences = len(sequences)
        for word, thumbnails in sequences:
            self._add_thumbnail_box(row_index, column_index, word, thumbnails)
            column_index += 1
            if column_index == num_columns:
                column_index = 0
                row_index += 1
        self.browser.currently_displaying_indicator_label.setText(
            f"Currently displaying level {level} sequences."
        )
        # update the number of currently displayed sequences in the label
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    def display_only_thumbnails_starting_with_letter(self, letter: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if letter != "Show all":
            self.browser.currently_displaying_indicator_label.setText(
                f"Currently displaying sequences starting with: {letter}. Please wait..."
            )
        self.browser.number_of_currently_displayed_sequences_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        base_words = self._get_sorted_base_words("sequence_length")
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3
        num_sequences = 0
        for word, thumbnails, seq_length in base_words:
            if len(letter) == 1:
                if word[0] != letter:
                    continue
            elif len(letter) == 2:
                if word[:2] != letter:
                    continue

            section = self.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))
            num_sequences += 1
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")
        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == num_columns:
                    column_index = 0
                    row_index += 1
        if letter != "Show all":
            self.browser.currently_displaying_indicator_label.setText(
                f"Currently displaying sequences starting with {letter}."
            )
        # update the number of currently displayed sequences in the label

        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    def _add_thumbnail_box(self, row_index, column_index, word, thumbnails):
        if word not in self.browser.scroll_widget.thumbnail_boxes_dict:
            thumbnail_box = ThumbnailBox(self.browser, word, thumbnails)
            thumbnail_box.resize_thumbnail_box()
            thumbnail_box.image_label.update_thumbnail(thumbnail_box.current_index)
            self.browser.scroll_widget.thumbnail_boxes_dict[word] = thumbnail_box

        thumbnail_box = self.browser.scroll_widget.thumbnail_boxes_dict[word]
        self.browser.scroll_widget.grid_layout.addWidget(
            thumbnail_box, row_index, column_index
        )
        QApplication.processEvents()

    def _get_sorted_base_words(self, sort_order):
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
            sequence_length = self.get_sequence_length_from_thumbnails(thumbnails)

            base_words[i] = (word, thumbnails, sequence_length)

        if sort_order == "sequence_length":
            base_words.sort(key=lambda x: x[2] if x[2] is not None else float("inf"))
        elif sort_order == "date_added":
            base_words.sort(
                key=lambda x: self.section_manager.get_date_added(x[1]) or datetime.min,
                reverse=True,
            )
        else:
            base_words.sort(key=lambda x: x[0])
        return base_words

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
