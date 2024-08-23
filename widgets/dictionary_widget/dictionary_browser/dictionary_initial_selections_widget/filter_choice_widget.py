from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class FilterChoiceWidget(QWidget):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget)
        self.initial_selection_widget = initial_selection_widget
        self.buttons: dict[str, QPushButton] = {}
        self.button_labels: dict[str, QLabel] = {}
        self.browser = initial_selection_widget.browser
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a descriptive label at the top
        self.description_label = QLabel(
            "Please choose a filter option below.\nEach option will display sequences based on the selected filter."
        )
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(4)
        main_layout.addWidget(self.description_label)
        main_layout.addStretch(1)

        # Create a grid layout for the filter options
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(
            50
        )  # Increased Horizontal space between columns
        grid_layout.setVerticalSpacing(30)  # Vertical space between rows
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Define filter options and their descriptions
        filter_options = [
            (
                "Starting Letter",
                "Display sequences that start with a specific letter.",
                self.initial_selection_widget.show_starting_letter_section,
            ),
            (
                "Contains Letter",
                "Display sequences that contain specific letters.",
                self.initial_selection_widget.show_contains_letter_section,
            ),
            (
                "Sequence Length",
                "Display sequences based on their length.",
                self.initial_selection_widget.show_length_section,
            ),
            (
                "Level",
                "Display sequences based on their difficulty level.",
                self.initial_selection_widget.show_level_section,
            ),
            (
                "Starting Position",
                "Display sequences based on their starting position.",
                self.initial_selection_widget.show_starting_position_section,
            ),
            (
                "Author",
                "Display sequences based on their author.",
                self.initial_selection_widget.show_author_section,
            ),
        ]

        # Add buttons and descriptions to the grid layout
        for index, (label, description, handler) in enumerate(filter_options):
            button = QPushButton(label)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(handler)
            self.buttons[label] = button

            description_label = QLabel(description)
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.button_labels[label] = description_label

            row = index // 3  # Calculate row number
            col = index % 3  # Calculate column number

            grid_layout.addWidget(
                button, row * 2, col, alignment=Qt.AlignmentFlag.AlignCenter
            )  # Add button to grid
            grid_layout.addWidget(
                description_label,
                row * 2 + 1,
                col,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )  # Add label below button

        main_layout.addLayout(grid_layout)

        # Add the "Show all sequences" button
        show_all_sequences_layout = QHBoxLayout()
        show_all_sequences_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        show_all_sequences_button = QPushButton("Show all")
        show_all_sequences_button.setCursor(Qt.CursorShape.PointingHandCursor)
        show_all_sequences_button.clicked.connect(
            self.initial_selection_widget.browser.show_all_sequences
        )
        self.buttons["Show all sequences"] = show_all_sequences_button
        show_all_sequences_layout.addWidget(show_all_sequences_button)

        main_layout.addStretch(2)
        main_layout.addLayout(show_all_sequences_layout)
        main_layout.addStretch(4)
        self.setLayout(main_layout)

    def resize_filter_choice_widget(self):
        self._resize_buttons_labels()
        self._resize_buttons()
        self._resize_description_label()

    def _resize_description_label(self):
        description_label_font = QFont()
        description_label_font.setPointSize(self.browser.width() // 90)
        self.description_label.setFont(description_label_font)

    def _resize_buttons(self):
        button_font = QFont()
        button_font.setPointSize(self.browser.width() // 80)
        for button in self.buttons.values():
            button.setFixedWidth(self.browser.width() // 7)
            button.setFixedHeight(self.browser.height() // 10)
            button.setFont(button_font)

    def _resize_buttons_labels(self):
        font = QFont()
        font.setPointSize(self.browser.width() // 170)
        for button_label in self.button_labels.values():
            button_label.setFont(font)
