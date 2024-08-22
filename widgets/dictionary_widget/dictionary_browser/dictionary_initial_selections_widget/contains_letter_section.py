from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem
from .filter_section_base import FilterSectionBase
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )

class ContainsLetterSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select Letters to be Contained:")
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
                        lambda checked, l=letter: self.initial_selection_widget.on_contains_letter_button_clicked(l)
                    )
                    button_row_layout.addWidget(button)
                layout.addLayout(button_row_layout)

            layout.addSpacerItem(
                QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            )

        apply_button_layout = QHBoxLayout()
        apply_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        apply_button = QPushButton("Apply Letter Filter")
        self.buttons["apply_contains_letter_filter"] = apply_button
        apply_button.clicked.connect(self.initial_selection_widget.apply_contains_letter_filter)
        apply_button_layout.addWidget(apply_button)
        layout.addLayout(apply_button_layout)

        layout.addStretch(1)
