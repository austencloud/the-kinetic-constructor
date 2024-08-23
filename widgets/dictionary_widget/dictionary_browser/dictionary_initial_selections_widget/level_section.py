from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QApplication,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter
import os

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
        self.image_placeholders: dict[str, QLabel] = {}
        self.scaled_images: dict[str, QPixmap] = {}  # Store scaled images
        self.images_loaded = False  # Flag to check if images are loaded
        self._add_buttons()

    def _add_buttons(self):
        layout: QVBoxLayout = self.layout()

        # Create a grid layout to hold the level buttons, descriptions, and images
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(50)
        grid_layout.setVerticalSpacing(30)  # Increased vertical spacing for clarity
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Level descriptions corresponding to each level
        level_descriptions = {
            1: "Level 1 sequences use all base letters with no extra turns.",
            2: "Level 2 sequences have turns added, but still have all radial orientations.",
            3: "Level 3 sequences use non-radial orientations.",
        }

        # Create buttons with descriptions and image placeholders
        available_levels = [1, 2, 3]
        for col, level in enumerate(available_levels):
            # Create a vertical box layout for each level's button, description, and image
            level_vbox = QVBoxLayout()
            level_vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Create the level button
            button = QPushButton(f"Level {level}")
            button.setFixedWidth(
                self.main_widget.width() // 5
            )  # Make the buttons wider
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

            # Placeholder for the image
            image_placeholder = QLabel()
            image_placeholder.setMinimumSize(
                self.main_widget.width() // 5, self.main_widget.height() // 8
            )
            image_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # Temporarily removing border to see if that helps
            # image_placeholder.setStyleSheet("border: 1px solid black;")

            # Store reference to image placeholders
            self.image_placeholders[f"level_{level}"] = image_placeholder

            # Add button, description, and image to the vertical box layout
            level_vbox.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            level_vbox.addWidget(
                description_label, alignment=Qt.AlignmentFlag.AlignCenter
            )
            level_vbox.addWidget(
                image_placeholder, alignment=Qt.AlignmentFlag.AlignCenter
            )

            # Add the vertical box layout to the grid layout
            grid_layout.addLayout(
                level_vbox, 0, col, alignment=Qt.AlignmentFlag.AlignCenter
            )

        # Add the grid layout to the main layout
        layout.addLayout(grid_layout)
        layout.addStretch(1)

    def load_and_display_images(self):
        if not self.images_loaded:
            self.load_images()  # Assuming load_images sets the pixmaps
            for placeholder in self.image_placeholders.values():
                placeholder.update()
                placeholder.repaint()
            self.images_loaded = True

    def load_images(self):
        """Load and scale images when the widget is shown."""
        if not self.images_loaded:
            image_dir = get_images_and_data_path("images\\level_images")
            for level, image_placeholder in self.image_placeholders.items():
                image_path = os.path.join(image_dir, f"{level}.png")
                if os.path.exists(image_path):
                    print(f"Loading image from: {image_path}")  # Debugging statement
                    pixmap = QPixmap(image_path)
                    scaled_pixmap = pixmap.scaled(
                        image_placeholder.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    image_placeholder.setPixmap(scaled_pixmap)
                    self.scaled_images[level] = scaled_pixmap
                    image_placeholder.adjustSize()  # Adjust size to fit the pixmap
                else:
                    print(f"Image not found at: {image_path}")  # Debugging statement
            self.images_loaded = True
            self.update()  # Force the widget to revalidate its display
            self.repaint()  # Ensure the widget repaints itself

    def resize_level_section(self):
        self.resize_level_buttons()
        self.resize_level_button_labels()
        self.resize_level_images()

    def resize_level_buttons(self):
        for button in self.buttons.values():
            button.setFixedWidth(self.browser.width() // 5)
            button.setFixedHeight(self.browser.height() // 10)

    def resize_level_button_labels(self):
        for label in self.labels.values():
            font = label.font()
            font.setPointSize(self.browser.height() // 80)
            label.setFont(font)

    def resize_level_images(self):
        if self.images_loaded:
            for level, image_placeholder in self.image_placeholders.items():
                image_placeholder.setMinimumSize(
                    self.browser.width() // 5, self.browser.height() // 8
                )
                if level in self.scaled_images:
                    scaled_pixmap = self.scaled_images[level].scaled(
                        image_placeholder.size(),
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                    image_placeholder.setPixmap(scaled_pixmap)
                    image_placeholder.adjustSize()  # Adjust size to fit the pixmap
            self.update()  # Ensure the widget updates its layout after resizing
            self.repaint()  # Repaint the widget to apply changes

