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
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QPainter, QPen

from utilities.path_helpers import get_images_and_data_path
from .filter_section_base import FilterSectionBase

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.initial_filter_selection_widget.dictionary_initial_selections_widget import (
        DictionaryInitialSelectionsWidget,
    )


class LevelSection(FilterSectionBase):
    def __init__(self, initial_selection_widget: "DictionaryInitialSelectionsWidget"):
        super().__init__(initial_selection_widget, "Select by Difficulty Level:")
        self.main_widget = initial_selection_widget.browser.main_widget
        self.buttons: dict[str, QPushButton] = {}
        self.labels: dict[str, QLabel] = {}
        self.level_images: dict[str, QLabel] = {}

    def add_buttons(self):
        self.initialized = True
        self.back_button.show()
        self.header_label.show()
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
                # Make the image clickable
                image_placeholder.setCursor(Qt.CursorShape.PointingHandCursor)
                image_placeholder.mousePressEvent = lambda event, l=level: self.initial_selection_widget.on_level_button_clicked(
                    l
                )
                # Install event filter for hover effect
                image_placeholder.installEventFilter(self)
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
        self.resize_level_section()


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

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_sequence_length(thumbnail)
            if length:
                return length
        return None

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

    def eventFilter(self, source, event):
        if isinstance(source, QLabel):
            if event.type() == QEvent.Type.Enter:
                # Save the original pixmap before modifying it
                self.original_pixmap = source.pixmap()
                if self.original_pixmap:
                    # Add a thicker gold border to the pixmap (e.g., 4 pixels)
                    bordered_pixmap = self.add_border_to_pixmap(self.original_pixmap, 4, Qt.GlobalColor.yellow)
                    source.setPixmap(bordered_pixmap)
            elif event.type() == QEvent.Type.Leave:
                # Reset to the original pixmap without the border
                if hasattr(self, 'original_pixmap') and self.original_pixmap:
                    source.setPixmap(self.original_pixmap)
        return super().eventFilter(source, event)

    def add_border_to_pixmap(self, pixmap, border_width, border_color):
        """Add a thicker border around the pixmap."""
        bordered_pixmap = QPixmap(pixmap.size())  # Create a new pixmap with the same size
        bordered_pixmap.fill(Qt.GlobalColor.transparent)  # Ensure the background is transparent
        painter = QPainter(bordered_pixmap)
        painter.drawPixmap(0, 0, pixmap)  # Draw the original pixmap onto the new pixmap

        # Set up the pen with the desired border color and width
        pen = QPen(border_color)
        pen.setWidth(border_width)
        painter.setPen(pen)

        # Draw the border around the pixmap, inset to ensure it stays within bounds
        painter.drawRect(border_width // 2, border_width // 2,
                         bordered_pixmap.width() - border_width,
                         bordered_pixmap.height() - border_width)
        painter.end()
        return bordered_pixmap

    def remove_border_from_pixmap(self, pixmap):
        """Remove the border by restoring the original pixmap."""
        # Assuming you have stored the original pixmap somewhere
        # For simplicity, you can maintain a dictionary with QLabel as key and original QPixmap as value
        return pixmap  # Replace with the stored original pixmap if available

    def scale_images(self):
        for level_image in self.level_images.values():
            pixmap = level_image.pixmap()
            if pixmap:
                size = self.browser.width() // 6
                scaled_pixmap = pixmap.scaled(
                    size,  # Desired width
                    size,  # Desired height
                    Qt.AspectRatioMode.KeepAspectRatio,  # Maintain aspect ratio
                    Qt.TransformationMode.SmoothTransformation,  # Smooth scaling
                )
                level_image.setPixmap(scaled_pixmap)

    def resize_level_section(self):
        self.scale_images()
        self.resize_buttons()
        self.resize_labels()

    def resize_labels(self):
        for label in self.labels.values():
            font = label.font()
            font.setPointSize(self.browser.width() // 140)
            label.setFont(font)
        font = self.header_label.font()
        font.setPointSize(self.browser.width() // 100)
        self.header_label.setFont(font)

    def resize_buttons(self):
        for button in self.buttons.values():
            font = button.font()
            font.setPointSize(self.browser.width() // 100)
            button.setFont(font)
            button.setFixedHeight(self.browser.height() // 20)
            button.setFixedWidth(self.browser.width() // 5)
