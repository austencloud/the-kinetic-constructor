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
        self.labels: dict[str, QLabel] = {}
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Add a descriptive label at the top
        self.description_label = QLabel(
            "Please choose a filter option below. Each option will display sequences based on the selected filter."
        )
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description_label = self.description_label
        main_layout.addWidget(self.description_label)

        # Define filter options and their descriptions
        filter_options = [
            (
                "Starting Letter",
                "Filter sequences by their starting letter.",
                self.initial_selection_widget.show_starting_letter_section,
            ),
            (
                "Contains Letter",
                "Filter sequences containing a specific letter.",
                self.initial_selection_widget.show_contains_letter_section,
            ),
            (
                "Sequence Length",
                "Filter sequences by their length.",
                self.initial_selection_widget.show_length_section,
            ),
            (
                "Level",
                "Filter sequences by difficulty level.",
                self.initial_selection_widget.show_level_section,
            ),
            (
                "Starting Position",
                "Filter sequences by their starting position.",
                self.initial_selection_widget.show_starting_position_section,
            ),
        ]

        # HBox layout for buttons
        button_layout = QHBoxLayout()

        # Add a spacer before the first button to center the buttons
        initial_spacer = QSpacerItem(
            20, 0, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
        )
        button_layout.addItem(initial_spacer)

        # Create buttons with descriptions below each
        for label, description, handler in filter_options:
            button_vbox = QVBoxLayout()
            button_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

            button = QPushButton(label)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(handler)
            self.buttons[label] = button

            # Add button and description to VBox layout
            button_vbox.addWidget(button)
            description_label = QLabel(description)
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            button_vbox.addWidget(description_label)
            self.labels[label] = description_label

            # Add the button VBox to the HBox layout
            button_layout.addLayout(button_vbox)

            # Add a spacer between buttons
            spacer = QSpacerItem(
                20, 0, QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum
            )
            button_layout.addItem(spacer)

        # Add the HBox layout to the main VBox layout
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def resize_labels(self, font_size: int):
        for label in self.labels.values():
            label.setFont(QFont("Arial", font_size))
