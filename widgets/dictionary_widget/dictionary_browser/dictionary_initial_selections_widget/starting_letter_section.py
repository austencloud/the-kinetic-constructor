from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QSizePolicy, QSpacerItem
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class StartingLetterSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Starting Letter:")
        self._add_buttons()
        self.browser = self.initial_selection_widget.browser
        self.currently_displaying_label = (
            self.initial_selection_widget.browser.currently_displaying_label
        )
        self.section_manager = self.browser.section_manager
        self.num_columns = self.browser.num_columns
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter
        self.main_widget = self.initial_selection_widget.browser.main_widget

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        sections = [
            [
                ["A", "B", "C", "D", "E", "F"],
                ["G", "H", "I", "J", "K", "L"],
                ["M", "N", "O", "P", "Q", "R"],
                ["S", "T", "U", "V"],
            ],
            [["W", "X", "Y", "Z"], ["Σ", "Δ", "θ", "Ω"]],
            [["W-", "X-", "Y-", "Z-"], ["Σ-", "Δ-", "θ-", "Ω-"]],
            [["Φ", "Ψ", "Λ"]],
            [["Φ-", "Ψ-", "Λ-"]],
            [["α", "β", "Γ"]],
            [["Show all"]],
        ]

        for section in sections:
            for row in section:
                button_row_layout = QHBoxLayout()
                button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                for letter in row:
                    button = QPushButton(letter)
                    button.setCursor(Qt.CursorShape.PointingHandCursor)
                    self.buttons[letter] = button
                    button.clicked.connect(
                        lambda checked, l=letter: self.initial_selection_widget.on_letter_button_clicked(
                            l
                        )
                    )
                    button_row_layout.addWidget(button)
                layout.addLayout(button_row_layout)
            layout.addSpacerItem(
                QSpacerItem(
                    20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
                )
            )
        layout.addStretch(1)

    ### STARTING LETTER ###

    def display_only_thumbnails_starting_with_letter(self, letter: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        if letter != "Show all":
            self.currently_displaying_label.show_loading_message(
                f"sequences starting with {letter}"
            )
        else:
            self.currently_displaying_label.show_loading_message("all sequences")

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

            if section not in self.browser.sections:
                self.browser.sections[section] = []

            self.browser.sections[section].append((word, thumbnails))
            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )

        sorted_sections = self.section_manager.get_sorted_sections(
            "sequence_length", self.browser.sections.keys()
        )
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")

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
        if letter != "Show all":
            self.currently_displaying_label.show_completed_message(
                f"sequences starting with {letter}"
            )
        else:
            self.currently_displaying_label.show_completed_message("all sequences")

        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words displayed: {num_words}"
        )
        self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
            self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )
        QApplication.restoreOverrideCursor()
