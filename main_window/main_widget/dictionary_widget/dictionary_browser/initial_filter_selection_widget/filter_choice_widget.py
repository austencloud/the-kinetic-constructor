from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QFont, QResizeEvent
from PyQt6.QtCore import Qt
from functools import partial
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from .dictionary_initial_selections_widget import DictionaryInitialSelectionsWidget


class FilterChoiceWidget(QWidget):
    """Widget to display filter options for the dictionary browser."""

    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget)
        self.initial_selection_widget = initial_selection_widget
        self.buttons: dict[str, QPushButton] = {}
        self.button_labels: dict[str, QLabel] = {}
        self.browser = initial_selection_widget.browser
        self.main_widget = initial_selection_widget.browser.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self._setup_ui()

    def _setup_ui(self):
        """Set up the UI components for the filter choice widget."""
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add a descriptive label at the top
        main_layout.addStretch(2)
        self.description_label = QLabel("Choose a filter:")
        self.description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.description_label)
        main_layout.addStretch(1)

        # Create a grid layout for the filter options
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Define filter options and their descriptions
        filter_options = [
            (
                "Starting Letter",
                "Display sequences that start with a specific letter.",
                partial(self.initial_selection_widget.show_section, "starting_letter"),
            ),
            (
                "Contains Letter",
                "Display sequences that contain specific letters.",
                partial(self.initial_selection_widget.show_section, "contains_letters"),
            ),
            (
                "Sequence Length",
                "Display sequences by length.",
                partial(self.initial_selection_widget.show_section, "sequence_length"),
            ),
            (
                "Level",
                "Display sequences by difficulty level.",
                partial(self.initial_selection_widget.show_section, "level"),
            ),
            (
                "Starting Position",
                "Display sequences by starting position.",
                partial(
                    self.initial_selection_widget.show_section, "starting_position"
                ),
            ),
            (
                "Author",
                "Display sequences by author.",
                partial(self.initial_selection_widget.show_section, "author"),
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

            row = index // 3  # Keep grid rows even
            col = index % 3  # Calculate column number

            grid_layout.addLayout(vbox, row, col)

        main_layout.addLayout(grid_layout)

        # Add "Show All" button and description at the bottom
        show_all_sequences_button = QPushButton("Show All")
        show_all_sequences_button.setCursor(Qt.CursorShape.PointingHandCursor)
        show_all_sequences_button.clicked.connect(
            self.initial_selection_widget.browser.show_all_sequences
        )
        self.buttons["Show All Sequences"] = show_all_sequences_button

        show_all_description_label = QLabel("Display every sequence in the dictionary.")
        show_all_description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button_labels["Show All Sequences"] = show_all_description_label

        # Create a vertical layout for the "Show All" button and its description
        show_all_vbox = QVBoxLayout()
        show_all_vbox.addWidget(
            show_all_sequences_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        show_all_vbox.addWidget(
            show_all_description_label, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Center the "Show All" button in the grid
        grid_layout.addLayout(show_all_vbox, 2, 1)

        main_layout.addStretch(2)
        self.setLayout(main_layout)

    def resize_filter_choice_widget(self):
        """Resize the filter choice widget and its components."""
        self._resize_buttons_labels()
        self._resize_buttons()
        self._resize_description_label()
        self._resize_all_labels_in_children()

    def _resize_all_labels_in_children(self):
        """Resize all labels in child sections to match font color."""
        for filter_choice_section in self.initial_selection_widget.section_map.values():
            if isinstance(
                filter_choice_section, FilterSectionBase
            ):  # Ensure it's a filter section
                for label in filter_choice_section.findChildren(QLabel):
                    font_color = (
                        self.settings_manager.global_settings.get_current_font_color()
                    )
                    label.setStyleSheet(f"color: {font_color};")

    def _resize_description_label(self):
        """Resize the main description label."""
        font_color = self.settings_manager.global_settings.get_current_font_color()
        font_size = self.main_widget.width() // 30
        font_family = "Monotype Corsiva"
        self.description_label.setStyleSheet(
            f"font-size: {font_size}px; color: {font_color}; font-family: {font_family};"
        )

    def _resize_buttons(self):
        """Resize the filter buttons."""
        button_font = QFont()
        button_font.setPointSize(self.main_widget.width() // 80)
        for button in self.buttons.values():
            button.setFixedWidth(self.main_widget.width() // 7)
            button.setFixedHeight(self.main_widget.height() // 10)
            button.setFont(button_font)

    def _resize_buttons_labels(self):
        """Resize the labels under each button."""
        font_size = self.main_widget.width() // 150
        font_color = self.settings_manager.global_settings.get_current_font_color()
        for button_label in self.button_labels.values():
            button_label.setStyleSheet(
                f"font-size: {font_size}px; color: {font_color};"
            )

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Handle resize events to adjust UI components."""
        self.resize_filter_choice_widget()
        super().resizeEvent(event)
