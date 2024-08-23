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

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        # Create a horizontal box layout for the starting position buttons
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hbox.addStretch(4)
        starting_positions = ["Alpha", "Beta", "Gamma"]
        for position in starting_positions:
            button = QPushButton(position.capitalize())
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"position_{position}"] = button
            button.clicked.connect(
                lambda checked, p=position: self.initial_selection_widget.on_position_button_clicked(
                    p
                )
            )
            hbox.addWidget(button)  # Add each button to the horizontal layout
            hbox.addStretch(1)
        hbox.addStretch(3)
        layout.addLayout(hbox)  # Add the horizontal layout to the main vertical layout
        layout.addStretch(1)

    def display_only_thumbnails_with_starting_position(self, position: str):
        self._prepare_ui_for_filtering(f"sequences starting at {position}")

        self.browser.currently_displayed_sequences = []
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        total_sequences = 0

        for word, thumbnails, seq_length in base_words:
            if self.get_sequence_starting_position(thumbnails) != position.lower():
                continue

            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )
            total_sequences += 1

        self._update_and_display_ui(" sequences starting at", total_sequences, position)

    def get_sequence_starting_position(self, thumbnails):
        """Extract the starting position from the first thumbnail (beat 0)."""
        for thumbnail in thumbnails:
            start_position = self.metadata_extractor.get_sequence_start_position(
                thumbnail
            )
            if start_position:
                return start_position
        return None
