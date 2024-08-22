from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
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
                        lambda checked, l=letter: self.initial_selection_widget.on_letter_button_clicked(l)
                    )
                    button_row_layout.addWidget(button)
                layout.addLayout(button_row_layout)

        layout.addStretch(1)
