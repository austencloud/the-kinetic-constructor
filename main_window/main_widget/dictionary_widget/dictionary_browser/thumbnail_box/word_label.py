from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QWidget,
    QHBoxLayout,
)
from PyQt6.QtGui import QFont, QIcon
from typing import TYPE_CHECKING
import os

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .thumbnail_box import ThumbnailBox


class WordLabel(QWidget):
    def __init__(self, thumbnail_box: "ThumbnailBox"):
        super().__init__(thumbnail_box)
        self.thumbnail_box = thumbnail_box
        self.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(60)  # Adjust the height as needed

        # Set up the word label
        self.word_label = QLabel(thumbnail_box.word)
        self.word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Set up the favorite button (star icon)
        self.favorite_button = QPushButton()
        self.favorite_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.favorite_button.setFlat(True)  # Remove button border

        # Load icons for the star button
        icons_path = get_images_and_data_path("images/icons")
        
        self.star_icon_empty_path = self.get_star_outline_icon()
        
        self.star_icon_empty = QIcon(os.path.join(icons_path, self.star_icon_empty_path))
        self.star_icon_filled = QIcon(os.path.join(icons_path, "star_filled.png"))

        # Connect the button click event to toggle the favorite status
        self.favorite_button.clicked.connect(self.thumbnail_box.toggle_favorite_status)

        # Create a layout for both the word and the star on the same line
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add an invisible spacer to the left to center the word label
        layout.addStretch(1)

        # Add the word label to the layout (centered)
        layout.addWidget(self.word_label)

        # Add the favorite button (aligned to the right)
        layout.addStretch(1)

        layout.addWidget(self.favorite_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Set the layout
        self.setLayout(layout)

    def reload_favorite_icon(self):
        # Reload the favorite icon based on the current favorite status
        self.star_icon_empty_path = self.get_star_outline_icon()
        self.star_icon_empty = QIcon(os.path.join(get_images_and_data_path("images/icons"), self.star_icon_empty_path))
        self.update_favorite_icon(self.thumbnail_box.favorite_status)

    def get_star_outline_icon(self):
        # Get the star outline icon based on the current theme
        if self.thumbnail_box.main_widget.main_window.settings_manager.global_settings.get_current_font_color() == "black":
            return "black_star_outline.png"
        elif self.thumbnail_box.main_widget.main_window.settings_manager.global_settings.get_current_font_color() == "white":
            return "white_star_outline.png"
        
    def resize_base_word_label(self):
        # Adjust the font size of the word label and the star button's icon size
        font_size = self.thumbnail_box.width() // 18
        font = QFont("Georgia", font_size, QFont.Weight.DemiBold)
        self.word_label.setFont(font)
        icon_size = QSize(font_size + 10, font_size + 10)
        self.favorite_button.setIconSize(icon_size)
        # Make sure the button is big enough to fit the icon
        self.favorite_button.setFixedSize(icon_size.width(), icon_size.height())

        # Manually offset the word label's position to account for the star button width
        offset = self.favorite_button.width()
        self.word_label.setStyleSheet(f"padding-left: {offset}px;")

    def update_favorite_icon(self, is_favorite: bool):
        # Update the favorite icon based on the favorite status
        if is_favorite:
            self.favorite_button.setIcon(self.star_icon_filled)
        else:
            self.favorite_button.setIcon(self.star_icon_empty)
