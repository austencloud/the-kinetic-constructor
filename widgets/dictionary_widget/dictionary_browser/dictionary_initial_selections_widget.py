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
        self.selected_letters: set[str] = set()  # Track selected letters for filtering
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)

        # Create separate widgets for each section
        starting_letter_widget = self._create_starting_letter_widget()
        contains_letter_widget = self._create_contains_letter_widget()
        length_widget = self._create_length_widget()
        level_widget = self._create_level_widget()

        # Add the widgets to the layoutBless you.
        layout.addWidget(starting_letter_widget)
        layout.addWidget(contains_letter_widget)
        layout.addWidget(length_widget)
        layout.addWidget(level_widget)

        self.setLayout(layout)

    def _create_starting_letter_widget(self):
        starting_letter_widget = QWidget()
        starting_letter_layout = QVBoxLayout(starting_letter_widget)
        self.starting_letter_label = QLabel("Select by Starting Letter:")
        self.starting_letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        starting_letter_layout.addWidget(self.starting_letter_label)
        starting_letter_layout.addStretch(1)

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
                button.setCursor(Qt.CursorShape.PointingHandCursor)

                self.buttons[letter] = button
                button.clicked.connect(
                    lambda checked, l=letter: self.on_letter_button_clicked(l)
                )
                button_row_layout.addWidget(button)
            starting_letter_layout.addLayout(button_row_layout)
        starting_letter_layout.addStretch(1)
        return starting_letter_widget

    def _create_length_widget(self):
        length_widget = QWidget()
        length_layout = QVBoxLayout(length_widget)
        length_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_label = QLabel("Select by Sequence Length:")
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        length_layout.addWidget(self.length_label)
        length_layout.addStretch(1)

        available_lengths = [4, 6, 8, 10, 12, 16, 20, 24, 28, 32]

        # Create buttons for each length in rows of 4
        for i in range(0, len(available_lengths), 4):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for length in available_lengths[i : i + 4]:
                button = QPushButton(str(length))
                button.setCursor(Qt.CursorShape.PointingHandCursor)
                self.buttons[f"length_{length}"] = button
                button.clicked.connect(
                    lambda checked, l=length: self.on_length_button_clicked(l)
                )
                hbox.addWidget(button)
            length_layout.addLayout(hbox)
        length_layout.addStretch(1)
        return length_widget

    def _create_contains_letter_widget(self):
        contains_letter_widget = QWidget()
        contains_letter_layout = QVBoxLayout(contains_letter_widget)
        self.contains_letter_label = QLabel("Select Letters to be Contained:")
        self.contains_letter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        contains_letter_layout.addWidget(self.contains_letter_label)
        contains_letter_layout.addStretch(1)

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
        ]

        # Create buttons for each row
        for row in rows:
            button_row_layout = QHBoxLayout()
            button_row_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            for letter in row:
                button = QPushButton(letter)
                button.setCursor(Qt.CursorShape.PointingHandCursor)

                self.buttons[f"contains_{letter}"] = button
                button.setCheckable(True)  # Button can be toggled
                button.clicked.connect(
                    lambda checked, l=letter: self.on_contains_letter_button_clicked(l)
                )
                button_row_layout.addWidget(button)
            contains_letter_layout.addLayout(button_row_layout)

        apply_button_layout = QHBoxLayout()
        apply_button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.apply_contains_letter_filter_button = QPushButton("Apply Letter Filter")
        self.apply_contains_letter_filter_button.clicked.connect(
            self.apply_contains_letter_filter
        )
        apply_button_layout.addWidget(self.apply_contains_letter_filter_button)
        contains_letter_layout.addLayout(apply_button_layout)
        contains_letter_layout.addStretch(1)

        return contains_letter_widget

    def _create_level_widget(self):
        level_widget = QWidget()
        level_layout = QVBoxLayout(level_widget)
        level_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.level_label = QLabel("Select by Level:")
        self.level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        level_layout.addWidget(self.level_label)
        level_layout.addStretch(1)

        available_levels = [1, 2, 3]

        for level in available_levels:
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button = QPushButton(f"Level {level}")
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            self.buttons[f"level_{level}"] = button
            button.clicked.connect(
                lambda checked, l=level: self.on_level_button_clicked(l)
            )
            hbox.addWidget(button)
            level_layout.addLayout(hbox)
        level_layout.addStretch(1)
        return level_widget

    def on_letter_button_clicked(self, letter: str):
        self.browser.apply_initial_selection({"letter": letter})

    def on_length_button_clicked(self, length: int):
        self.browser.apply_initial_selection({"length": length})

    def on_level_button_clicked(self, level: int):
        self.browser.apply_initial_selection({"level": level})

    def on_contains_letter_button_clicked(self, letter: str):
        if letter in self.selected_letters:
            self.selected_letters.remove(letter)
        else:
            self.selected_letters.add(letter)

    def apply_contains_letter_filter(self):
        self.browser.apply_initial_selection(
            {"contains_letters": self.selected_letters}
        )

    def resizeEvent(self, event):
        self._resize_starting_letter_section()
        self._resize_length_section()
        self._resize_level_section()
        self._resize_contains_letter_section()
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

    def _resize_starting_letter_section(self):
        font = self.starting_letter_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.starting_letter_label.setFont(font)
        for button in self.buttons.values():
            button.setMaximumWidth(self.browser.width() // 10)
            font = button.font()
            font.setPointSize(self.browser.width() // 100)
            button.setFont(font)

    def _resize_contains_letter_section(self):
        font = self.contains_letter_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.contains_letter_label.setFont(font)
        for key, button in self.buttons.items():
            if "contains_" in key:
                button.setMaximumWidth(self.browser.width() // 10)
                font = button.font()
                font.setPointSize(self.browser.width() // 100)
                button.setFont(font)
        # set the font size of the apply button
        font = self.apply_contains_letter_filter_button.font()
        font.setPointSize(self.browser.width() // 100)
        self.apply_contains_letter_filter_button.setFont(font)
