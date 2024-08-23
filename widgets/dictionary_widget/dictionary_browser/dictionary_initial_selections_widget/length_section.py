from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class LengthSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Sequence Length:")
        self._add_buttons()
        self.browser = self.initial_selection_widget.browser
        self.currently_displaying_label = (
            self.initial_selection_widget.browser.currently_displaying_label
        )
        self.section_manager = self.browser.section_manager
        self.num_columns = self.browser.num_columns
        self.metadata_extractor = self.browser.main_widget.metadata_extractor
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        available_lengths = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]
        for i in range(0, len(available_lengths), 4):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for length in available_lengths[i : i + 4]:
                button = QPushButton(str(length))
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.buttons[f"length_{length}"] = button
                button.clicked.connect(
                    lambda checked, l=length: self.initial_selection_widget.on_length_button_clicked(
                        l
                    )
                )
                hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)

    def display_only_thumbnails_with_sequence_length(self, length: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self.currently_displaying_label.show_loading_message(
            f"sequences of length {length}"
        )
        self.browser.number_of_currently_displayed_words_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.browser.sections = {}
        self.browser.currently_displayed_sequences = (
            []
        )  # Reset the list for the new filter
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        row_index = 0
        num_words = 0

        for word, thumbnails, seq_length in base_words:
            if seq_length != length:
                continue

            section = self.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.browser.sections:
                self.browser.sections[section] = []

            self.browser.sections[section].append((word, thumbnails))
            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )  # Update currently displayed sequences

        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.browser.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")
        QApplication.processEvents()

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
        self.currently_displaying_label.show_completed_message(
            f"sequences of length {length}"
        )
        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words displayed: {num_words}"
        )
        QApplication.restoreOverrideCursor()
