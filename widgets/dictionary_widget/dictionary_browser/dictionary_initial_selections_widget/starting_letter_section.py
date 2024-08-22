from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
)
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class StartingLetterSection(QWidget):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget)
        self.buttons: dict[str, QPushButton] = {}
        self.initial_selection_widget = initial_selection_widget
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        self.starting_letter_label = QLabel("Select by Starting Letter:")
        self.starting_letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.starting_letter_label)
        layout.addStretch(1)

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
