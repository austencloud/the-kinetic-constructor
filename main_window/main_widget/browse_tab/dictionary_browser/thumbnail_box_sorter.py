import os
from datetime import datetime
from typing import TYPE_CHECKING
from main_window.main_widget.browse_tab.dictionary_browser.thumbnail_box.thumbnail_box import (
    ThumbnailBox,
)
from utilities.path_helpers import get_images_and_data_path
from PyQt6.QtWidgets import QApplication

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_browser.dictionary_browser import (
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

    def reload_currently_displayed_filtered_sequences(self):
        current_filter = (
            self.browser.dictionary.dictionary_settings.get_current_filter()
        )
        self.browser.thumbnail_box_sorter.sort_and_display_thumbnail_boxes_by_current_filter(
            current_filter
        )

    def sort_and_display_currently_filtered_sequences_by_method(
        self, sort_method: str
    ) -> None:
        self.browser.scroll_widget.clear_layout()
        self.browser.sections = {}
        if sort_method == "sequence_length":
            self.browser.currently_displayed_sequences.sort(
                key=lambda x: x[2] if x[2] is not None else float("inf")
            )
        elif sort_method == "date_added":
            self.browser.currently_displayed_sequences.sort(
                key=lambda x: self.section_manager.get_date_added(x[1]) or datetime.min,
                reverse=True,
            )
        else:
            self.browser.currently_displayed_sequences.sort(key=lambda x: x[0])

        row_index = 0
        for word, thumbnails, seq_length in self.browser.currently_displayed_sequences:
            section = self.section_manager.get_section_from_word(
                word, sort_method, seq_length, thumbnails
            )

            if section not in self.browser.sections:
                self.browser.sections[section] = []

            self.browser.sections[section].append((word, thumbnails))

        sorted_sections = self.section_manager.get_sorted_sections(
            sort_method, self.browser.sections.keys()
        )

        self.browser.nav_sidebar.update_sidebar(sorted_sections, sort_method)
        current_section = None

        self.browser.options_widget.sort_widget.highlight_appropriate_button(
            sort_method
        )

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

            column_index = 0  # Reset column index at the start of each section

            for word, thumbnails in self.browser.sections[section]:
                self.add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1

        self.browser.sequence_count_label.setText(
            f"Number of words: {len(self.browser.currently_displayed_sequences)}"
        )
        QApplication.restoreOverrideCursor()

    def sort_and_display_thumbnail_boxes_by_current_filter(
        self, initial_selection: dict
    ):
        initial_selection_widget = self.browser.initial_selection_widget

        starting_position_section = initial_selection_widget.starting_position_section
        contains_letter_section = initial_selection_widget.contains_letter_section
        starting_letter_section = initial_selection_widget.starting_letter_section
        level_section = initial_selection_widget.level_section
        length_section = initial_selection_widget.length_section
        author_section = initial_selection_widget.author_section
        grid_mode_section = initial_selection_widget.grid_mode_section
        display_functions = {
            "starting_letter": starting_letter_section.display_only_thumbnails_starting_with_letter,
            "sequence_length": length_section.display_only_thumbnails_with_sequence_length,
            "level": level_section.display_only_thumbnails_with_level,
            "contains_letters": contains_letter_section.display_only_thumbnails_containing_letters,
            "starting_position": starting_position_section.display_only_thumbnails_with_starting_position,
            "author": author_section.display_only_thumbnails_by_author,
            "favorites": self.browser.filter_manager.show_favorites,
            "most_recent": self.browser.filter_manager.show_most_recent_sequences,
            "grid_mode": grid_mode_section.display_only_thumbnails_with_grid_mode,
            "show_all": self.browser.filter_manager.show_all_sequences,
        }
        if initial_selection:
            for key, value in initial_selection.items():
                if key in display_functions:
                    if key in ["favorites", "show_all"]:
                        display_functions[key]()
                    else:
                        display_functions[key](value)
        self.browser.initialized = True

    ### HELPER FUNCTIONS ###

    def add_thumbnail_box(
        self, row_index, column_index, word, thumbnails, hidden: bool = False
    ):
        if word not in self.browser.scroll_widget.thumbnail_boxes:
            thumbnail_box = ThumbnailBox(self.browser, word, thumbnails)
            thumbnail_box.resize_thumbnail_box()
            thumbnail_box.image_label.update_thumbnail(thumbnail_box.current_index)
            self.browser.scroll_widget.thumbnail_boxes[word] = thumbnail_box
        else:
            thumbnail_box = self.browser.scroll_widget.thumbnail_boxes[word]

        if hidden:
            thumbnail_box.hide()

        self.browser.scroll_widget.grid_layout.addWidget(
            thumbnail_box, row_index, column_index
        )

        if not hidden:
            thumbnail_box.show()

    def get_sorted_base_words(self, sort_order):
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

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_sequence_length(thumbnail)
            if length:
                return length
        return None
