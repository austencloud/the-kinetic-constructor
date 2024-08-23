from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
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
        self.browser = initial_selection_widget.browser
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a descriptive label at the top
        self.description_label = QLabel("Choose a filter:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch(4)
        main_layout.addWidget(self.description_label)
        main_layout.addStretch(2)

        # Create a grid layout for the filter options
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(20)
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

            # Create a vertical layout for each button and its description
            vbox = QVBoxLayout()
            vbox.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            vbox.addWidget(description_label, alignment=Qt.AlignmentFlag.AlignCenter)

            row = index // 3 * 2  # Calculate row number (doubled for spacing)
            col = index % 3  # Calculate column number

            grid_layout.addLayout(vbox, row, col)

        # Add an empty row between the first and second rows of buttons
        self.grid_spacer_item_1 = QSpacerItem(
            0,
            0,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.MinimumExpanding,
        )
        grid_layout.addItem(
            self.grid_spacer_item_1, 1, 0, 1, 3
        )  # Add spacer across all three columns

        main_layout.addLayout(grid_layout)

        # Add the "Show all sequences" button to the grid layout
        show_all_sequences_button = QPushButton("Show all")
        show_all_sequences_button.setCursor(Qt.CursorShape.PointingHandCursor)
        show_all_sequences_button.clicked.connect(
            self.initial_selection_widget.browser.show_all_sequences
        )
        self.buttons["Show all sequences"] = show_all_sequences_button

        # add a spacer item between the grid layout and the button
        self.grid_spacer_item_2 = QSpacerItem(
            0,
            0,
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.MinimumExpanding,
        )
        grid_layout.addItem(
            self.grid_spacer_item_2, 3, 0, 1, 3
        )  # Add spacer across all three columns

        # Add the button below the middle column in the grid layout
        grid_layout.addWidget(
            show_all_sequences_button, 4, 1, alignment=Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addStretch(4)
        self.setLayout(main_layout)

    def resize_filter_choice_widget(self):
        self._resize_buttons_labels()
        self._resize_buttons()
        self._resize_description_label()
        self._resize_grid_spacer_items()

    def _resize_grid_spacer_items(self):
        self.grid_spacer_item_1.changeSize(0, self.height() // 15)
        self.grid_spacer_item_2.changeSize(0, self.height() // 15)

    def _resize_description_label(self):
        description_label_font = QFont()
        description_label_font.setFamily("Monotype Corsiva")
        description_label_font.setPointSize(self.browser.width() // 60)
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
