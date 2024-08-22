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
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add a descriptive label at the top
        self.description_label = QLabel(
            "Please choose a filter option below.\nEach option will display sequences based on the selected filter."
        )
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label = self.description_label
        main_layout.addStretch(4)
        main_layout.addWidget(self.description_label)
        main_layout.addStretch(1)

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
        ]
        show_all_sequences_layout = QHBoxLayout()
        show_all_sequences_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        show_all_sequences_button = QPushButton("Show all")
        show_all_sequences_button.setCursor(Qt.CursorShape.PointingHandCursor)
        show_all_sequences_button.clicked.connect(
            self.initial_selection_widget.browser.show_all_sequences
        )
        self.buttons["Show all sequences"] = show_all_sequences_button
        show_all_sequences_layout.addWidget(show_all_sequences_button)
        # HBox layout for buttons
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Add a spacer before the first button to center the buttons
        button_layout.addStretch(1)

        # Create buttons with descriptions below each
        for label, description, handler in filter_options:
            button_vbox = QVBoxLayout()
            button_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

            button = QPushButton(label)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(handler)
            self.buttons[label] = button

            button_vbox.addWidget(button)
            description_label = QLabel(description)
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_vbox.addWidget(description_label)
            self.button_labels[label] = description_label

            button_layout.addLayout(button_vbox)

            button_layout.addStretch(1)
        main_layout.addLayout(button_layout)
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
        description_label_font.setPointSize(self.initial_selection_widget.width() // 90)
        self.description_label.setFont(description_label_font)

    def _resize_buttons(self):
        button_font = QFont()
        button_font.setPointSize(self.initial_selection_widget.width() // 80)
        for button in self.buttons.values():
            button.setFixedWidth(self.initial_selection_widget.width() // 6)
            button.setMinimumHeight(self.initial_selection_widget.height() // 10)
            button.setFont(button_font)

    def _resize_buttons_labels(self):
        font = QFont()
        font.setPointSize(self.initial_selection_widget.width() // 170)
        for button_label in self.button_labels.values():
            button_label.setFont(font)
