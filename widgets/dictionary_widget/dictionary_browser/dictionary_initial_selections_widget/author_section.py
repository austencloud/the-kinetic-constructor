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
        self.initialized = False

    def add_buttons(self):
        self.authors = self._get_unique_authors()  # Get a list of unique authors
        self.initialized = True
        self.back_button.show()
        self.label.show()
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


    def display_only_thumbnails_by_author(self, author: str):
        self._prepare_ui_for_filtering(f"sequences by {author}")

        self.browser.currently_displayed_sequences = []
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("author")
        total_sequences = 0

        for word, thumbnails, seq_length in base_words:
            sequence_author = self.main_widget.metadata_extractor.get_sequence_author(
                thumbnails[0]
            )
            if sequence_author != author:
                continue

            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )
            total_sequences += 1

        self._update_and_display_ui(" sequences by", total_sequences, author)
