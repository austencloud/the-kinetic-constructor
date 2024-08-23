from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QApplication
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class StartingPositionSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Starting Position:")
        self._add_buttons()
        self.browser = self.initial_selection_widget.browser
        self.currently_displaying_label = (
            self.initial_selection_widget.browser.currently_displaying_label
        )
        self.thumbnail_box_sorter = self.browser.thumbnail_box_sorter
        self.metadata_extractor = self.browser.main_widget.metadata_extractor

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        starting_positions = ["alpha", "beta", "gamma"]
        for position in starting_positions:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(position.capitalize())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"position_{position}"] = button
            button.clicked.connect(
                lambda checked, p=position: self.initial_selection_widget.on_position_button_clicked(
                    p
                )
            )
            hbox.addWidget(button)
            layout.addLayout(hbox)

        layout.addStretch(1)

    def display_only_thumbnails_with_starting_position(self, position: str):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.currently_displaying_label.show_loading_message(
            f"sequences starting at {position}"
        )
        self.browser.number_of_currently_displayed_words_label.setText("")

        self.browser.scroll_widget.clear_layout()
        self.thumbnail_box_sorter.sections = {}
        self.browser.currently_displayed_sequences = []
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        row_index = 0
        num_words = 0

        for word, thumbnails, seq_length in base_words:
            if self.get_sequence_starting_position(thumbnails) != position:
                continue

            section = self.browser.section_manager.get_section_from_word(
                word, "sequence_length", seq_length, thumbnails
            )

            if section not in self.thumbnail_box_sorter.sections:
                self.thumbnail_box_sorter.sections[section] = []

            self.thumbnail_box_sorter.sections[section].append((word, thumbnails))
            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )
            num_words += 1
            self.browser.number_of_currently_displayed_words_label.setText(
                f"Number of words displayed: {num_words}"
            )
            QApplication.processEvents()
        sorted_sections = self.browser.section_manager.get_sorted_sections(
            "sequence_length", self.thumbnail_box_sorter.sections.keys()
        )

        # Update the navigation sidebar with the filtered and sorted sections
        self.browser.nav_sidebar.update_sidebar(sorted_sections, "sequence_length")

        QApplication.processEvents()

        for section in sorted_sections:
            row_index += 1
            self.browser.section_manager.add_header(
                row_index, self.thumbnail_box_sorter.num_columns, section
            )
            row_index += 1

            column_index = 0
            for word, thumbnails in self.thumbnail_box_sorter.sections[section]:
                self.thumbnail_box_sorter.add_thumbnail_box(
                    row_index, column_index, word, thumbnails
                )
                column_index += 1
                if column_index == self.thumbnail_box_sorter.num_columns:
                    column_index = 0
                    row_index += 1

        self.currently_displaying_label.show_completed_message(
            f"sequences starting at {position}"
        )
        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words displayed: {num_words}"
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
