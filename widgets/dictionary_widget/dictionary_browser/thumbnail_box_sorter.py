import os
from datetime import datetime
from typing import TYPE_CHECKING
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
from widgets.path_helpers.path_helpers import get_images_and_data_path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from .currently_displaying_indicator_label import CurrentlyDisplayingIndicatorLabel

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
        self.currently_displaying_label = browser.currently_displaying_label
        self.num_columns = 3
        self.currently_displayed_sequences = []

    def sort_and_display_currently_filtered_sequences_by_method(
        self, sort_method: str
    ) -> None:
        self.browser.scroll_widget.clear_layout()
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}

        # Sort currently displayed sequences based on the sort_method
        if sort_method == "sequence_length":
            self.currently_displayed_sequences.sort(
                key=lambda x: x[2] if x[2] is not None else float("inf")
            )
        elif sort_method == "date_added":
            self.currently_displayed_sequences.sort(
                key=lambda x: self.section_manager.get_date_added(x[1]) or datetime.min,
                reverse=True,
            )
        else:
            self.currently_displayed_sequences.sort(key=lambda x: x[0])

        row_index = 0
        for word, thumbnails, seq_length in self.currently_displayed_sequences:
            section = self.section_manager.get_section_from_word(
                word, sort_method, seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))

        sorted_sections = self.section_manager.get_sorted_sections(
            sort_method, self.sections.keys()
        )

        # Update the navigation sidebar with the filtered and sorted sections
        self.browser.nav_sidebar.update_sidebar(sorted_sections, sort_method)

        QApplication.processEvents()
        current_section = None

        for section in sorted_sections:
            # if the sort method is date added, remove the year. It's like 07-24-2024, so we can safely remove the last five characters before giving the section a name
            if sort_method == "date_added":
                if section == "Unknown":
                    continue

                day, month, year = section.split("-")
                formatted_day = f"{int(day)}-{int(month)}"

                if year != current_section:
                    row_index += 1
                    self.section_manager.add_header(row_index, self.num_columns, year)
                    row_index += 1
                    current_section = year

                row_index += 1
                self.section_manager.add_header(
                    row_index, self.num_columns, formatted_day
                )
                row_index += 1
            else:
                row_index += 1
                self.section_manager.add_header(row_index, self.num_columns, section)
                row_index += 1

            column_index = 0  # Reset column index at the start of each section

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {len(self.currently_displayed_sequences)}"
        )
        QApplication.restoreOverrideCursor()

    def sort_and_display_all_thumbnail_boxes_by_sort_method(
        self, sort_method: str
    ) -> None:
        self.currently_displaying_label.show_loading_message("all sequences")
        self.browser.options_widget.sort_widget.highlight_appropriate_button(
            sort_method
        )
        self.browser.scroll_widget.clear_layout()
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}

        base_words = self._get_sorted_base_words(sort_method)
        self.currently_displayed_sequences = base_words  # Track all sequences

        current_section = None
        row_index = 0
        column_index = 0
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
                    self.section_manager.add_header(row_index, self.num_columns, year)
                    row_index += 1
                    current_section = year

                row_index += 1
                self.section_manager.add_header(
                    row_index, self.num_columns, formatted_day
                )
                row_index += 1
            else:
                row_index += 1
                self.section_manager.add_header(row_index, self.num_columns, section)
                row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        self.currently_displaying_label.show_completed_message("all sequences")
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {len(base_words)}"
        )

    def sort_and_display_thumbnail_boxes_by_initial_selection(
        self, initial_selection: dict
    ):
        if "letter" in initial_selection:
            self.display_only_thumbnails_starting_with_letter(
                initial_selection["letter"]
            )
        elif "length" in initial_selection:
            self.display_only_thumbnails_with_sequence_length(
                initial_selection["length"]
            )
        elif "level" in initial_selection:
            self.display_only_thumbnails_with_level(initial_selection["level"])
        elif "contains_letters" in initial_selection:
            self.display_only_thumbnails_containing_letters(
                initial_selection["contains_letters"]
            )
        elif "position" in initial_selection:
            self.display_only_thumbnails_with_starting_position(
                initial_selection["position"]
            )

    ### STARTING LETTER ###

    def display_only_thumbnails_starting_with_letter(self, letter: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if letter != "Show all":
            self.currently_displaying_label.show_loading_message(
                f"sequences starting with {letter}"
            )
        else:
            self.currently_displaying_label.show_loading_message("all sequences")

        self.browser.number_of_currently_displayed_sequences_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        self.currently_displayed_sequences = []  # Reset the list for the new filter
        base_words = self._get_sorted_base_words("sequence_length")
        row_index = 0
        num_sequences = 0

        for word, thumbnails, seq_length in base_words:
            if len(letter) == 1:
                if word[0] != letter:
                    continue
                elif len(word) > 1 and word[1] == "-":
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
            self.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )  # Update currently displayed sequences
            num_sequences += 1
            #update the number of sequences displayed
            self.browser.number_of_currently_displayed_sequences_label.setText(
                f"Number of sequences displayed: {num_sequences}"
            )
            QApplication.processEvents()
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")

        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        if letter != "Show all":
            self.currently_displaying_label.show_completed_message(
                f"sequences starting with {letter}"
            )
        else:
            self.currently_displaying_label.show_completed_message("all sequences")

        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    ### CONTAINING LETTERS ###

    def display_only_thumbnails_containing_letters(self, letters: set[str]):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        letters_string = ", ".join(letters)
        self.currently_displaying_label.show_loading_message(
            f"sequences containing {letters_string}"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        self.currently_displayed_sequences = []  # Reset the list for the new filter
        base_words = self._get_sorted_base_words("sequence_length")
        row_index = 0
        num_sequences = 0

        for word, thumbnails, seq_length in base_words:
            match_found = False

            for letter in letters:
                if self._is_valid_letter_match(word, letter, letters):
                    match_found = True
                    break

            if not match_found:
                continue

            section = self.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))
            self.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )  # Update currently displayed sequences
            num_sequences += 1
            self.browser.number_of_currently_displayed_sequences_label.setText(
                f"Number of sequences displayed: {num_sequences}"
            )
            QApplication.processEvents()
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")

        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        self.currently_displaying_label.show_completed_message(
            f"sequences containing {letters_string}"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    ### SEQUENCE LENGTH ###

    def display_only_thumbnails_with_sequence_length(self, length: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.currently_displaying_label.show_loading_message(
            f"sequences of length {length}"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        self.currently_displayed_sequences = []  # Reset the list for the new filter
        base_words = self._get_sorted_base_words("sequence_length")
        row_index = 0
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
            self.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )  # Update currently displayed sequences
            num_sequences += 1
            self.browser.number_of_currently_displayed_sequences_label.setText(
                f"Number of sequences displayed: {num_sequences}"
            )
            QApplication.processEvents()
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")
        QApplication.processEvents()

        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        self.currently_displaying_label.show_completed_message(
            f"sequences of length {length}"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_sequence_length(thumbnail)
            if length:
                return length
        return None

    ### LEVEL ###

    def display_only_thumbnails_with_level(self, level: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.currently_displaying_label.show_loading_message(f"level {level} sequences")
        self.browser.number_of_currently_displayed_sequences_label.setText("")
        self.browser.scroll_widget.clear_layout()
        sequences = self.get_sequences_that_are_a_specific_level(level)
        row_index = 0
        column_index = 0
        num_sequences = len(sequences)
        for word, thumbnails in sequences:
            self._add_thumbnail_box(row_index, column_index, word, thumbnails)
            column_index += 1
            if column_index == self.num_columns:
                column_index = 0
                row_index += 1
        # add the sequences to the currently_displayed_sequences list, including the word, thumbnails, seq_length
        self.currently_displayed_sequences = [
            (word, thumbnails, self.get_sequence_length_from_thumbnails(thumbnails))
            for word, thumbnails in sequences
        ]

        self.currently_displaying_label.show_completed_message(
            f"level {level} sequences"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
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

    ### STARTING POSITION ###

    def display_only_thumbnails_with_starting_position(self, position: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.currently_displaying_label.show_loading_message(
            f"sequences starting at {position}"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.sections = {}
        self.currently_displayed_sequences = []  # Reset the list for the new filter
        base_words = self._get_sorted_base_words("sequence_length")
        row_index = 0
        num_sequences = 0

        for word, thumbnails, seq_length in base_words:
            if self.get_sequence_starting_position(thumbnails) != position:
                continue

            section = self.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.sections:
                self.sections[section] = []

            self.sections[section].append((word, thumbnails))
            self.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )  # Update currently displayed sequences
            num_sequences += 1
            # updatethe number of sequences displayed
            self.browser.number_of_currently_displayed_sequences_label.setText(
                f"Number of sequences displayed: {num_sequences}"
            )
            QApplication.processEvents()
        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.sections.keys()
        )

        # Update the navigation sidebar with the filtered and sorted sections
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")

        QApplication.processEvents()

        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, section)
            row_index += 1

            column_index = 0
            for word, thumbnails in self.sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        self.currently_displaying_label.show_completed_message(
            f"sequences starting at {position}"
        )
        self.browser.number_of_currently_displayed_sequences_label.setText(
            f"Number of sequences displayed: {num_sequences}"
        )
        QApplication.restoreOverrideCursor()

    def get_sequence_starting_position(self, thumbnails):
        """Extract the starting position from the first thumbnail (beat 0)."""
        for thumbnail in thumbnails:
            start_position = self.metadata_extractor.get_sequence_start_position(
                thumbnail
            )
            if start_position:
                return start_position
        return None

    ### HELPER FUNCTIONS ###

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

    def _is_valid_letter_match(self, word, letter, letters):
        if letter in word:
            if (
                len(letter) == 1
                and f"{letter}-" in word
                and f"{letter}-" not in letters
            ):
                return False
            if (
                len(letter) != 2):
                if letter + "-" in word and letter + "-" not in letters:
                    return False
                if word.find(letter) < len(word) - 1 and word[word.find(letter) + 1] == "-":
                    return False
            return True
        return False
