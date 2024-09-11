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
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class StartingLetterSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Starting Letter:")

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
        self.resize_starting_letter_section()

    def display_only_thumbnails_starting_with_letter(self, letter: str):
        description = (
            f"sequences starting with {letter}"
            if letter != "Show all"
            else "all sequences"
        )
        self.browser.nav_sidebar.clear_sidebar()
        QApplication.processEvents()
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

            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, seq_length)
            )
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
            # clear the nav buttons widget

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
                self.progress_bar.setValue(percentage)
                self.browser.number_of_currently_displayed_words_label.setText(
                    f"Number of words: {num_words}"
                )
                QApplication.processEvents()

            self.progress_bar.setVisible(False)

            self.thumbnail_box_sorter.sort_and_display_currently_filtered_sequences_by_method(
                self.main_widget.main_window.settings_manager.dictionary_settings.get_sort_method()
            )

            self.browser.currently_displaying_label.show_completed_message(
                f" sequences starting with", letter
            )
            QApplication.restoreOverrideCursor()

        QTimer.singleShot(0, update_ui)
        self.initial_selection_widget.browser.dictionary_widget.dictionary_settings.set_current_filter(
            "starting_letter"
        )

    def resize_starting_letter_section(self):
        self.resize_buttons()
        self.resize_label()

    def resize_label(self):
        font = self.header_label.font()
        font.setPointSize(self.browser.main_widget.width() // 100)
        self.header_label.setFont(font)

    def resize_buttons(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(self.browser.main_widget.width() // 100)
            button.setFont(font)
            button.setFixedHeight(self.browser.main_widget.height() // 20)
            button.setFixedWidth(self.browser.main_widget.width() // 20)
