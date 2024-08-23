import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QPushButton,
    QLabel,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QCursor

from widgets.path_helpers.path_helpers import get_images_and_data_path
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_initial_selections_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class LevelSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Level:")
        self.main_widget = initial_selection_widget.browser.main_widget
        self.buttons: dict[str, QPushButton] = {}
        self.labels: dict[str, QLabel] = {}
        self.level_images: dict[str, QLabel] = {}
        self.initialized: bool = False

    def add_buttons(self):
        self.initialized = True
        self.back_button.show()
        self.label.show()
        layout: QVBoxLayout = self.layout()

        # Create a grid layout to hold the level buttons, descriptions, and images
        grid_layout = QGridLayout()
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)

        # Level descriptions corresponding to each level
        level_descriptions = {
            1: "Base letters with no turns.",
            2: "Turns added with only radial orientations.",
            3: "Non-radial orientations.",
        }

        # Path where level images are stored
        image_dir = get_images_and_data_path("images/level_images")

        # Create buttons, descriptions, and images
        available_levels = [1, 2, 3]
        for col, level in enumerate(available_levels):
            # Create a vertical box layout for each level's button, description, and image
            level_vbox = QVBoxLayout()
            level_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create the level button
            button = QPushButton(f"Level {level}")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            self.buttons[f"level_{level}"] = button
            button.clicked.connect(
                lambda checked, l=level: self.initial_selection_widget.on_level_button_clicked(
                    l
                )
            )

            # Create a label for the description
            description_label = QLabel(level_descriptions[level])
            description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.labels[f"level_{level}"] = description_label

            # Create the image placeholder
            image_placeholder = QLabel()
            image_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.level_images[f"level_{level}"] = image_placeholder

            # Load and set the image
            image_path = os.path.join(image_dir, f"level_{level}.png")
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                image_placeholder.setPixmap(pixmap)
            else:
                image_placeholder.setText("No Image Available")

            # Add button, description, and image to the grid layout
            grid_layout.addWidget(button, 0, col)
            grid_layout.addWidget(description_label, 1, col)

            # Add a spacer between the description and the image
            spacer_item = QSpacerItem(
                20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
            grid_layout.addItem(spacer_item, 2, col)

            grid_layout.addWidget(image_placeholder, 3, col)

        # Add the grid layout to the main layout
        layout.addLayout(grid_layout)
        layout.addStretch(1)

    def display_only_thumbnails_with_level(self, level: str):
        self._prepare_ui_for_filtering(f"level {level} sequences")

        self.browser.currently_displayed_sequences = []
        sequences = self.get_sequences_that_are_a_specific_level(level)
        total_sequences = len(sequences)

        for word, thumbnails in sequences:
            self.browser.currently_displayed_sequences.append(
                (word, thumbnails, self.get_sequence_length_from_thumbnails(thumbnails))
            )

        self._update_and_display_ui("level", total_sequences, level)

    def get_sequences_that_are_a_specific_level(self, level: str):
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (
                d,
                self.main_widget.thumbnail_finder.find_thumbnails(
                    os.path.join(dictionary_dir, d)
                ),
                None,
            )
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d)) and "__pycache__" not in d
        ]

        for i, (word, thumbnails, _) in enumerate(base_words):
            sequence_level = self.get_sequence_level_from_thumbnails(thumbnails)
            base_words[i] = (word, thumbnails, sequence_level)

        return [
            (word, thumbnails)
            for word, thumbnails, sequence_level in base_words
            if sequence_level == level
        ]

    def get_sequence_level_from_thumbnails(self, thumbnails):
        for thumbnail in thumbnails:
            level = self.metadata_extractor.get_sequence_level(thumbnail)
            if level:
                return level
        return None

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_sequence_length(thumbnail)
            if length:
                return length
        return None

    def scale_images(self):
        for level_image in self.level_images:
            image = self.level_images[level_image]
            pixmap = image.pixmap()
            if pixmap:
                size = self.browser.width() // 6
                scaled_pixmap = pixmap.scaled(
                    size,  # Desired width
                    size,  # Desired height
                    Qt.AspectRatioMode.KeepAspectRatio,  # Maintain aspect ratio
                    Qt.TransformationMode.SmoothTransformation,  # Smooth scaling
                )
                image.setPixmap(scaled_pixmap)

    def resize_level_section(self):
        self.scale_images()
        self.resize_buttons()
        self.resize_label_fonts()

    def resize_label_fonts(self):
        for label in self.labels.values():
            font = label.font()
            font.setPointSize(self.browser.width() // 140)
            label.setFont(font)

    def resize_buttons(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(self.browser.width() // 100)
            button.setFont(font)
            button.setFixedHeight(self.browser.height() // 20)
            button.setFixedWidth(self.browser.width() // 5)
