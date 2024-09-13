from typing import TYPE_CHECKING, Iterable
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QApplication,
    QWidget,
)
from PyQt6.QtCore import Qt, QTimer
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from .dictionary_initial_selections_widget import DictionaryInitialSelectionsWidget


class ContainsLettersSection(FilterSectionBase):
    SECTIONS = [
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
    ]

    LETTER_ORDER = [letter for section in SECTIONS for row in section for letter in row]

    FONT_SIZE_FACTOR = 100
    BUTTON_SIZE_FACTOR = 20
    APPLY_BUTTON_WIDTH_FACTOR = 6

    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select letters to be contained:")
        self.main_widget = initial_selection_widget.browser.main_widget
        self.selected_letters: set[str] = set()
        self.buttons: dict[str, QPushButton] = {}
        self.add_buttons()

    def add_buttons(self):
        self.initialized = True
        self.back_button.show()
        self.header_label.show()

        layout: QVBoxLayout = self.layout()

        # Create letter buttons
        self.create_letter_buttons(layout)

        # Sequence tally label
        layout.addStretch(1)
        self.sequence_tally_label = QLabel("0 sequences")
        self.sequence_tally_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sequence_tally_label)
        layout.addStretch(1)

        # Apply button
        apply_button_layout = QHBoxLayout()
        apply_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_filter)
        apply_button_layout.addWidget(self.apply_button)
        layout.addLayout(apply_button_layout)

        layout.addStretch(1)
        self.resize_contains_letters_section()

    def create_letter_buttons(self, layout: QVBoxLayout):
        for section in self.SECTIONS:
            for row_data in section:
                button_row_layout = QHBoxLayout()
                button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                for letter in row_data:
                    button = QPushButton(letter)
                    button.setCursor(Qt.CursorShape.PointingHandCursor)
                    button.setCheckable(True)
                    button.setProperty("letter", letter)
                    button.clicked.connect(self.update_letter_selection)
                    self.buttons[letter] = button
                    button_row_layout.addWidget(button)
                layout.addLayout(button_row_layout)

    def update_letter_selection(self):
        """Update the selected letters and the sequence tally."""
        self.selected_letters = {
            button.property("letter")
            for button in self.buttons.values()
            if button.isChecked()
        }

        matching_sequences = self._count_sequences_matching_selected_letters()
        sequence_text = "sequence" if matching_sequences == 1 else "sequences"
        self.sequence_tally_label.setText(f"{matching_sequences} {sequence_text}")

    def _count_sequences_matching_selected_letters(self) -> int:
        """Count the number of sequences that match the currently selected letters."""
        if not self.selected_letters:
            return 0

        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        return sum(
            any(letter in word for letter in self.selected_letters)
            for word, _, _ in base_words
        )

    def apply_filter(self):
        """Apply the filter based on the selected letters."""
        self.initial_selection_widget.apply_contains_letter_filter(
            list(self.selected_letters)
        )

    def display_only_thumbnails_containing_letters(self, letters: list[str]):
        """Display only the thumbnails that contain the specified letters."""
        letters = self.organize_letters(letters)
        display_letters = self.format_display_letters(letters)

        self._prepare_ui_for_filtering(f" sequences containing\n {display_letters}")

        sort_method = (
            self.main_widget.main_window.settings_manager.dictionary_settings.get_sort_method()
        )
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")

        matching_sequences = [
            (word, thumbnails, seq_length)
            for word, thumbnails, seq_length in base_words
            if any(
                self._is_valid_letter_match(word, letter, letters) for letter in letters
            )
        ]

        total_sequences = len(matching_sequences) or 1
        self.browser.currently_displayed_sequences = matching_sequences
        self.browser.number_of_sequences_label.setText(
            f"Number of words to be displayed: {len(matching_sequences)}"
        )

        def update_ui():
            for index, (word, thumbnails, _) in enumerate(matching_sequences):
                row_index = index // self.thumbnail_box_sorter.num_columns
                column_index = index % self.thumbnail_box_sorter.num_columns
                self.thumbnail_box_sorter.add_thumbnail_box(
                    row_index=row_index,
                    column_index=column_index,
                    word=word,
                    thumbnails=thumbnails,
                    hidden=True,
                )
                percentage = int(((index + 1) / total_sequences) * 100)
                self.progress_bar.setValue(percentage)
                self.browser.number_of_sequences_label.setText(
                    f"Number of words: {index + 1}"
                )
                QApplication.processEvents()

            self.progress_bar.setVisible(False)
            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                sort_method
            )
            self.browser.currently_displaying_label.show_completed_message(
                " sequences containing\n", display_letters
            )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)
        self.initial_selection_widget.browser.dictionary_widget.dictionary_settings.set_current_filter(
            {"contains_letters": letters}
        )

    def organize_letters(self, letters: Iterable[str]) -> list[str]:
        """Organize letters according to the predefined order."""
        letters_set = set(letters)
        return [letter for letter in self.LETTER_ORDER if letter in letters_set]

    def format_display_letters(self, letters: list[str]) -> str:
        """Format the display letters for UI."""
        if len(letters) == 1:
            return letters[0]
        elif len(letters) == 2:
            return f"{letters[0]} or {letters[1]}"
        else:
            return ", ".join(letters[:-1]) + ", or " + letters[-1]

    def _is_valid_letter_match(
        self, word: str, letter: str, letters: list[str]
    ) -> bool:
        """Check if a letter is a valid match in the word."""
        if letter not in word:
            return False

        letter_with_dash = f"{letter}-"
        if len(letter) == 1:
            if letter_with_dash in word and letter_with_dash not in letters:
                return False
            if word.endswith(letter_with_dash) and letter_with_dash not in letters:
                return False
            index = word.find(letter)
            if index != -1 and index < len(word) - 1 and word[index + 1] == "-":
                return False
        else:
            if letter_with_dash in word and letter_with_dash not in letters:
                return False

        return True

    def resize_contains_letters_section(self):
        self.resize_widget_font(self.header_label)
        self.resize_widget_font(self.sequence_tally_label)
        self.resize_buttons()
        self.resize_apply_button()

    def resize_widget_font(self, widget: QWidget):
        font = widget.font()
        font.setPointSize(self.main_widget.width() // self.FONT_SIZE_FACTOR)
        widget.setFont(font)

    def resize_buttons(self):
        width = self.main_widget.width() // self.BUTTON_SIZE_FACTOR
        height = self.main_widget.height() // self.BUTTON_SIZE_FACTOR
        font_size = self.main_widget.width() // self.FONT_SIZE_FACTOR
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.setFixedSize(width, height)

    def resize_apply_button(self):
        width = self.main_widget.width() // self.APPLY_BUTTON_WIDTH_FACTOR
        self.apply_button.setFixedWidth(width)
        self.resize_widget_font(self.apply_button)
