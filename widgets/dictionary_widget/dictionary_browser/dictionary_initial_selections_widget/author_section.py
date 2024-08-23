from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class AuthorSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Author:")
        self.browser = self.initial_selection_widget.browser
        self.currently_displaying_label = (
            self.initial_selection_widget.browser.currently_displaying_label
        )
        self.section_manager = self.browser.section_manager
        self.num_columns = self.browser.num_columns
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter
        self.main_widget = self.initial_selection_widget.browser.main_widget
        self.authors = self._get_unique_authors()  # Get a list of unique authors
        self._add_buttons()

    def _get_unique_authors(self):
        """Extract unique authors from all sequences."""
        authors = set()
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("author")
        for word, thumbnails, seq_length in base_words:
            author = self.main_widget.metadata_extractor.get_sequence_author(
                thumbnails[0]
            )
            if author:
                authors.add(author)
        return sorted(authors)

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        for author in self.authors:
            button_row_layout = QHBoxLayout()
            button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(author)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[author] = button
            button.clicked.connect(
                lambda checked, a=author: self.initial_selection_widget.on_author_button_clicked(
                    a
                )
            )
            button_row_layout.addWidget(button)
            layout.addLayout(button_row_layout)

        layout.addStretch(1)

    def display_only_thumbnails_by_author(self, author: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.currently_displaying_label.show_loading_message(f"sequences by {author}")

        self.browser.number_of_currently_displayed_words_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.browser.sections = {}
        self.browser.currently_displayed_sequences = []
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("author")
        row_index = 0
        num_words = 0

        for word, thumbnails, seq_length in base_words:
            sequence_author = self.main_widget.metadata_extractor.get_sequence_author(
                thumbnails[0]
            )
            if sequence_author != author:
                continue

            section = self.section_manager.get_section_from_word(
                word, "author", seq_length, thumbnails
            )

            if section not in self.browser.sections:
                self.browser.sections[section] = []

            self.browser.sections[section].append((word, thumbnails))
            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )

        sorted_sections = self.section_manager.get_sorted_sections(
            "author", self.browser.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "author")

        for section in sorted_sections:
            row_index += 1
            self.section_manager.add_header(row_index, self.num_columns, section)
            row_index += 1

            column_index = 0

            for word, thumbnails in self.browser.sections[section]:
                self.thumbnail_box_sorter.add_thumbnail_box(
                    row_index, column_index, word, thumbnails
                )
                column_index += 1
                if column_index == self.num_columns:
                    column_index = 0
                    row_index += 1
                num_words += 1
                self.browser.number_of_currently_displayed_words_label.setText(
                    f"Number of words displayed: {num_words}"
                )
                QApplication.processEvents()

        self.currently_displaying_label.show_completed_message(f"sequences by {author}")
        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words displayed: {num_words}"
        )
        self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
            self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )
        QApplication.restoreOverrideCursor()
