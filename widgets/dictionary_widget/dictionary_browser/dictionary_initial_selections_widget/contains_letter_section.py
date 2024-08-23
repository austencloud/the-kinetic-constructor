from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QApplication,
    QProgressBar,
)
from PyQt6.QtCore import Qt, QTimer

from widgets.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
    RainbowProgressBar,
)

from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from ..dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class ContainsLetterSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select Letters to be Contained:")

    def add_buttons(self):
        self.initialized = True
        self.back_button.show()
        self.header_label.show()

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
        ]

        for section in sections:
            for row in section:
                button_row_layout = QHBoxLayout()
                button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                for letter in row:
                    button = QPushButton(letter)
                    button.setCursor(Qt.CursorShape.PointingHandCursor)
                    button.setCheckable(True)
                    self.buttons[f"contains_{letter}"] = button
                    button.clicked.connect(
                        lambda checked, l=letter: self.initial_selection_widget.on_contains_letter_button_clicked(
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

        apply_button_layout = QHBoxLayout()
        apply_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_button = QPushButton("Apply Letter Filter")
        self.apply_button.clicked.connect(
            self.initial_selection_widget.apply_contains_letter_filter
        )
        apply_button_layout.addWidget(self.apply_button)
        layout.addLayout(apply_button_layout)

        layout.addStretch(1)
        self.resize_contains_letter_section()

    def display_only_thumbnails_containing_letters(self, letters: set[str]):
        letters = self.organize_letters(letters)
        self._prepare_ui_for_filtering(f"sequences containing \n{', '.join(letters)}")

        self.browser.currently_displayed_sequences = []
        sort_method = (
            self.main_widget.main_window.settings_manager.dictionary.get_sort_method()
        )
        base_words = self.thumbnail_box_sorter.get_sorted_base_words(sort_method)
        total_sequences = 0

        for word, thumbnails, seq_length in base_words:
            if any(
                self._is_valid_letter_match(word, letter, letters) for letter in letters
            ):
                self.browser.currently_displayed_sequences.append(
                    (word, thumbnails, seq_length)
                )
                total_sequences += 1

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
                    f"Number of words: {num_words}"
                )
                QApplication.processEvents()

            self.loading_progress_bar.setVisible(False)
            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                sort_method
            )

            self.browser.currently_displaying_label.show_completed_message(
                " sequences containing\n", ", ".join(letters)
            )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)

    def organize_letters(self, letters: set[str]) -> list[str]:
        letter_order = [
            ["A", "B", "C", "D", "E", "F"],
            ["G", "H", "I", "J", "K", "L"],
            ["M", "N", "O", "P", "Q", "R"],
            ["S", "T", "U", "V"],
            ["W", "X", "Y", "Z"],
            ["Σ", "Δ", "θ", "Ω"],
            ["W-", "X-", "Y-", "Z-"],
            ["Σ-", "Δ-", "θ-", "Ω-"],
            ["Φ", "Ψ", "Λ"],
            ["Φ-", "Ψ-", "Λ-"],
            ["α", "β", "Γ"],
        ]
        # make it so the letters are in the order they appear in the UI
        ordered_letters = []
        for row in letter_order:
            for letter in row:
                if letter in letters:
                    ordered_letters.append(letter)
        return ordered_letters

    def _is_valid_letter_match(self, word, letter, letters):
        if letter in word:
            if (
                len(letter) == 1
                and f"{letter}-" in word
                and f"{letter}-" not in letters
            ):
                return False
            if len(letter) != 2:
                if letter + "-" in word and letter + "-" not in letters:
                    return False
                if (
                    word.find(letter) < len(word) - 1
                    and word[word.find(letter) + 1] == "-"
                ):
                    return False
            return True
        return False

    def resize_contains_letter_section(self):
        self.resize_buttons()
        self.resize_label()

    def resize_label(self):
        font = self.header_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.header_label.setFont(font)

    def resize_buttons(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(self.browser.width() // 120)
            button.setFont(font)
            button.setFixedHeight(self.browser.height() // 24)
            button.setFixedWidth(self.browser.width() // 24)
        self.apply_button.setFixedWidth(self.browser.width() // 6)
        apply_button_font = self.apply_button.font()
        apply_button_font.setPointSize(self.browser.width() // 100)
        self.apply_button.setFont(apply_button_font)
