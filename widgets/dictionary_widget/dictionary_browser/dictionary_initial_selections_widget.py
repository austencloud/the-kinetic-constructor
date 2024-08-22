from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
)
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionaryInitialSelectionsWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser"):
        super().__init__(browser)
        self.browser = browser
        self.buttons: dict[str, QPushButton] = {}
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        # Create separate widgets for each section
        letter_widget = self._create_letter_widget()
        length_widget = self._create_length_widget()
        level_widget = self._create_level_widget()

        # Add the widgets to the layout with equal stretch
        layout.addWidget(letter_widget, 1)
        layout.addWidget(length_widget, 1)
        layout.addWidget(level_widget, 1)

        self.setLayout(layout)

    def _create_letter_widget(self):
        letter_widget = QWidget()
        letter_layout = QVBoxLayout(letter_widget)
        self.letter_label = QLabel("Select by Starting Letter:")
        self.letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        letter_layout.addWidget(self.letter_label)
        letter_layout.addStretch(1)
        # Define the rows of letters
        rows = [
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
            ["Show all"],
        ]

        # Create buttons for each row
        for row in rows:
            button_row_layout = QHBoxLayout()
            button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for letter in row:
                button = QPushButton(letter)
                self.buttons[letter] = button
                button.clicked.connect(
                    lambda checked, l=letter: self.on_letter_button_clicked(l)
                )
                button_row_layout.addWidget(button)
            letter_layout.addLayout(button_row_layout)
        letter_layout.addStretch(1)
        return letter_widget

    def _create_length_widget(self):
        length_widget = QWidget()
        length_layout = QVBoxLayout(length_widget)
        length_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_label = QLabel("Select by Sequence Length:")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        length_layout.addWidget(self.length_label)
        length_layout.addStretch(1)
        # Example lengths - in a real scenario, these would be dynamically determined
        available_lengths = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]

        for length in available_lengths:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(str(length))
            self.buttons[f"length_{length}"] = button
            button.clicked.connect(
                lambda checked, l=length: self.on_length_button_clicked(l)
            )
            hbox.addWidget(button)
            length_layout.addLayout(hbox)
            length_layout.addStretch(1)
        return length_widget

    def _create_level_widget(self):
        level_widget = QWidget()
        level_layout = QVBoxLayout(level_widget)
        level_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label = QLabel("Select by Level:")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        level_layout.addWidget(self.level_label)
        level_layout.addStretch(1)
        # Example levels - in a real scenario, these would be dynamically determined
        available_levels = [1, 2, 3]

        for level in available_levels:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(f"Level {level}")

            self.buttons[f"level_{level}"] = button
            button.clicked.connect(
                lambda checked, l=level: self.on_level_button_clicked(l)
            )
            hbox.addWidget(button)
            level_layout.addLayout(hbox)
            level_layout.addStretch(1)
        return level_widget

    def on_letter_button_clicked(self, letter: str):
        # When a letter button is clicked, immediately apply the selection to filter words
        self.browser.apply_initial_selection({"letter": letter})

    def on_length_button_clicked(self, length: int):
        # When a length button is clicked, immediately apply the selection to filter by sequence length
        self.browser.apply_initial_selection({"length": length})

    def on_level_button_clicked(self, level: int):
        # When a level button is clicked, immediately apply the selection to filter by level
        self.browser.apply_initial_selection({"level": level})

    def resizeEvent(self, event):
        self._resize_letter_section()
        self._resize_length_section()
        self._resize_level_section()
        super().resizeEvent(event)

    def _resize_level_section(self):
        font = self.level_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.level_label.setFont(font)
        for key, button in self.buttons.items():
            if "level_" in key:
                button.setFont(font)

    def _resize_length_section(self):
        font = self.length_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.length_label.setFont(font)
        for key, button in self.buttons.items():
            if "length_" in key:
                button.setFont(font)

    def _resize_letter_section(self):
        font = self.letter_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.letter_label.setFont(font)
        for button in self.buttons.values():
            button.setMaximumWidth(self.browser.width() // 10)
            font = button.font()
            font.setPointSize(self.browser.width() // 100)
            button.setFont(font)
