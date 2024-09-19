from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QWidget,
    QApplication,
)
from PyQt6.QtCore import Qt, QEvent, QObject
from PyQt6.QtGui import QFontMetrics
from .filter_section_base import FilterSectionBase
from functools import partial

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class StartingLetterSection(FilterSectionBase):
    SECTIONS: List[List[List[str]]] = [
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

    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by starting letter:")
        self.main_widget = initial_selection_widget.browser.main_widget
        self.buttons: Dict[str, QPushButton] = {}
        self.sequence_tally: Dict[str, int] = {}
        self.sequence_tally_label = QLabel("")
        self.add_buttons()

    def add_buttons(self):
        self.initialized = True
        self.back_button.show()
        self.header_label.show()

        layout: QVBoxLayout = self.layout()
        self.create_letter_buttons(layout)

        # Add stretch after buttons
        layout.addStretch(1)

        # Initialize sequence tally
        self.sequence_tally = self._get_starting_letter_sequence_counts()

        # Label to display the sequence count when hovering
        self.sequence_tally_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sequence_tally_label)

        layout.addStretch(1)
        self.resize_starting_letter_section()

    def create_letter_buttons(self, layout: QVBoxLayout):
        for section in self.SECTIONS:
            for row in section:
                button_row_layout = QHBoxLayout()
                button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                for letter in row:
                    button = self.create_letter_button(letter)
                    button_row_layout.addWidget(button)
                layout.addLayout(button_row_layout)

    def create_letter_button(self, letter: str) -> QPushButton:
        """Create a QPushButton for a given letter."""
        button = QPushButton(letter)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.buttons[letter] = button
        button.setProperty("letter", letter)
        button.installEventFilter(self)
        # Use partial to pass the letter to the slot
        button.clicked.connect(
            partial(
                self.initial_selection_widget.on_starting_letter_button_clicked,
                letter,
            )
        )
        return button

    def _get_starting_letter_sequence_counts(self) -> Dict[str, int]:
        """Tally up how many sequences start with each letter."""
        letter_counts = {letter: 0 for letter in self.buttons.keys()}
        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")

        for word, _, _ in base_words:
            first_letter = self.extract_first_letter(word)
            if first_letter in letter_counts:
                letter_counts[first_letter] += 1

        return letter_counts

    @staticmethod
    def extract_first_letter(word: str) -> str:
        """Extract the first letter or symbol from the word."""
        if len(word) > 1 and word[1] == "-":
            return word[:2]
        return word[0]

    def display_only_thumbnails_starting_with_letter(self, letter: str):
        """Display thumbnails of sequences starting with the specified letter."""
        self.initial_selection_widget.browser.dictionary_widget.dictionary_settings.set_current_filter(
            {"starting_letter": letter}
        )

        description = (
            f"sequences starting with {letter}"
            if letter != "show_all"
            else "all sequences"
        )
        self.browser.nav_sidebar.clear_sidebar()
        QApplication.processEvents()
        self.browser.prepare_ui_for_filtering(description)

        base_words = self.thumbnail_box_sorter.get_sorted_base_words("sequence_length")
        if letter == "show_all":
            matching_sequences = [
                (word, thumbnails, seq_length)
                for word, thumbnails, seq_length in base_words
            ]
        else:
            matching_sequences = [
                (word, thumbnails, seq_length)
                for word, thumbnails, seq_length in base_words
                if self._word_starts_with_letter(word, letter)
            ]

        total_sequences = len(matching_sequences) or 1  # Prevent division by zero
        self.browser.currently_displayed_sequences = matching_sequences
        self.browser.update_and_display_ui(total_sequences, letter)

    def _word_starts_with_letter(self, word: str, letter: str) -> bool:
        """Check if the word starts with the given letter."""
        if len(letter) == 1:
            return word.startswith(letter) and (len(word) == 1 or word[1] != "-")
        return word.startswith(letter)



    def resize_starting_letter_section(self):
        self.resize_buttons()
        self.resize_widget_font(self.header_label, 100)
        self.resize_widget_font(self.sequence_tally_label, 100)
        self.sequence_tally_label.setMinimumHeight(self.calculate_label_height())

    def resize_widget_font(self, widget: QWidget, factor: int):
        font = widget.font()
        font.setPointSize(max(10, self.main_widget.width() // factor))
        widget.setFont(font)

    def resize_buttons(self):
        width = self.main_widget.width() // 20
        height = self.main_widget.height() // 20
        font_size = max(10, self.main_widget.width() // 100)
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(font_size)
            button.setFont(font)
            button.setFixedSize(width, height)

    def calculate_label_height(self) -> int:
        """Calculate and return the height needed for the label."""
        font = self.sequence_tally_label.font()
        font.setPointSize(max(10, self.main_widget.width() // 100))
        font_metrics = QFontMetrics(font)
        return int(font_metrics.height() * 2.1)

    # Event filter to handle hover events
    def eventFilter(self, obj: QObject, event: QEvent):
        if event.type() == QEvent.Type.Enter:
            letter = obj.property("letter")
            count = self.sequence_tally.get(letter, 0)
            sequence_text = "sequence" if count == 1 else "sequences"
            self.sequence_tally_label.setText(f"{letter}:\n{count} {sequence_text}")
        elif event.type() == QEvent.Type.Leave:
            self.sequence_tally_label.clear()
        return super().eventFilter(obj, event)
