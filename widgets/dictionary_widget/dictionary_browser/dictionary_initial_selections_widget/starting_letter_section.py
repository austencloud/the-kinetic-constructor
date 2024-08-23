from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QApplication,
    QSizePolicy,
    QSpacerItem,
)
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt, QTimer

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class StartingLetterSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Starting Letter:")
        self._add_buttons()

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        sections = [
            [["A", "B", "C", "D", "E", "F"],
             ["G", "H", "I", "J", "K", "L"],
             ["M", "N", "O", "P", "Q", "R"],
             ["S", "T", "U", "V"]],
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

    def display_only_thumbnails_starting_with_letter(self, letter: str):
        description = f"sequences starting with {letter}" if letter != "Show all" else "all sequences"
        self._prepare_ui_for_filtering(description)

        self.browser.currently_displayed_sequences = []
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        total_sequences = 0

        for word, thumbnails, seq_length in base_words:
            if len(letter) == 1:
                if word[0] != letter or (len(word) > 1 and word[1] == "-"):
                    continue
            elif len(letter) == 2:
                if word[:2] != letter:
                    continue

            self.browser.currently_displayed_sequences.append((word, thumbnails, seq_length))
            total_sequences += 1

        self._update_and_display_ui(total_sequences, letter)

    def _update_and_display_ui(self, total_sequences, letter):
        if total_sequences == 0:
            total_sequences = 1  # Prevent division by zero

        self.browser.number_of_currently_displayed_words_label.setText(
            f"Number of words to be displayed: {total_sequences}"
        )

        def update_ui():
            num_words = 0

            for index, (word, thumbnails, _) in enumerate(
                self.browser.currently_displayed_sequences
            ):
                row_index = index // self.thumbnail_box_sorter.num_columns
                column_index = index % self.thumbnail_box_sorter.num_columns
                self.thumbnail_box_sorter.add_thumbnail_box(
                    row_index=row_index,
                    column_index=column_index,
                    word=word,
                    thumbnails=thumbnails,
                    hidden=True,
                )
                num_words += 1

                percentage = int((num_words / total_sequences) * 100)
                self.loading_progress_bar.setValue(percentage)
                self.browser.number_of_currently_displayed_words_label.setText(
                    f"Number of words displayed: {num_words}"
                )
                QApplication.processEvents()

            self.loading_progress_bar.setVisible(False)

            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
            )

            self.browser.currently_displaying_label.show_completed_message(
                f"sequences starting with {letter}"
            )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)
