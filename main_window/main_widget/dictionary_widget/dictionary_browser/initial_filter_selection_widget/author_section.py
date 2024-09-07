from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class AuthorSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Author:")

    def add_buttons(self):
        self.authors = self._get_unique_authors()  # Get a list of unique authors
        self.initialized = True
        self.back_button.show()
        self.header_label.show()
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
        self.resize_author_section()

    def _get_unique_authors(self):
        """Extract unique authors from all sequences."""
        authors = set()
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("author")
        for _, thumbnails, _ in base_words:
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

    def resize_author_section(self):
        self.resize_buttons()
        self.resize_labels()

    def resize_labels(self):
        font = self.header_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.header_label.setFont(font)

    def resize_buttons(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(self.browser.width() // 100)
            button.setFont(font)
            button.setFixedHeight(self.browser.height() // 20)
            button.setFixedWidth(self.browser.width() // 5)
