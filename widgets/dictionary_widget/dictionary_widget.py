import os
from typing import TYPE_CHECKING
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QStyle, QMessageBox
from PyQt6.QtCore import Qt, QSize
from path_helpers import get_images_and_data_path
from widgets.dictionary_widget.dictionary_sequence_populator import (
    DictionarySequencePopulator,
)
from widgets.dictionary_widget.thumbnail_box import ThumbnailBox
from .dictionary_variation_manager import DictionaryVariationManager

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class DictionaryWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.setup_ui()
        self.variation_manager = DictionaryVariationManager(self)
        self.sequence_populator = DictionarySequencePopulator(self)
        self.selected_thumbnail = (
            None  # Initialize the attribute to avoid AttributeError
        )

    def setup_ui(self):
        # Using a horizontal layout to split the dictionary and preview area
        h_layout = QHBoxLayout(self)

        # Creating a widget for the dictionary area
        dictionary_area = QWidget()
        dictionary_layout = QVBoxLayout(dictionary_area)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setHorizontalSpacing(20)
        self.scroll_layout.setVerticalSpacing(20)
        self.scroll_area.setWidget(self.scroll_content)
        dictionary_layout.addWidget(self.scroll_area)
        h_layout.addWidget(
            dictionary_area, 3
        )  # Dictionary area takes 3 parts of the space

        # Creating a widget for the preview area
        preview_area = QWidget()
        preview_layout = QVBoxLayout(preview_area)
        self.preview_label = QLabel("Select a thumbnail to display it here.")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.preview_label)

        # Buttons for editing and other actions
        self.edit_button = QPushButton("Edit Sequence")
        self.edit_button.clicked.connect(self.edit_sequence)
        preview_layout.addWidget(self.edit_button)

        # TODO: Implement other buttons as needed and connect their clicked signals

        h_layout.addWidget(preview_area, 2)  # Preview area takes 2 parts of the space
        self.setLayout(h_layout)
        self.load_base_words()

    def edit_sequence(self):
        if self.selected_thumbnail:
            # This now calls the load sequence method from the sequence populator
            self.sequence_populator.load_sequence_from_thumbnail(
                self.selected_thumbnail
            )
            # Switch to the builder tab, assuming you have a way to reference it:
            self.main_widget.setCurrentIndex(self.main_widget.builder_tab_index)
        else:
            QMessageBox.warning(
                self, "No Selection", "Please select a thumbnail first."
            )

    def get_metadata_from_thumbnail(self, thumbnail):
        # This is a placeholder, you need to implement logic to extract metadata from the thumbnail
        return {"file_path": "path_to_the_sequence_file.json"}

    def thumbnail_clicked(self, thumbnail_pixmap, metadata):
        # Save the thumbnail metadata when a thumbnail is clicked
        self.selected_thumbnail = metadata
        # Update the preview area with the selected thumbnail pixmap
        self.preview_label.setPixmap(
            thumbnail_pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def load_base_words(self):
        dictionary_dir = get_images_and_data_path("dictionary")
        if not os.path.exists(dictionary_dir):
            os.makedirs(dictionary_dir)
        base_words = [
            d
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d))
        ]

        # Debug: Check that base_words is not empty
        print(f"Base words: {base_words}")

        for i, word in enumerate(base_words):
            thumbnails = self.find_thumbnails(os.path.join(dictionary_dir, word))
            # Debug: Ensure thumbnails have valid image paths
            print(f"Thumbnails for {word}: {thumbnails}")

            if thumbnails:
                thumbnail_box = ThumbnailBox(self, word, thumbnails)
                self.scroll_layout.addWidget(thumbnail_box, i // 3, i % 3)
            else:
                button = QPushButton(word)
                button.clicked.connect(lambda _, w=word: self.show_variations(w))
                self.scroll_layout.addWidget(button, i // 3, i % 3)

        # Ensure layout is set after adding widgets
        self.scroll_content.setLayout(self.scroll_layout)
        self.update()  # Refresh UI after layout update

    def thumbnail_area_width(self):
        # Get the available width for a single row of thumbnails.
        scrollbar_width = 0
        if self.scroll_area.verticalScrollBar().isVisible():
            scrollbar_width = self.scroll_area.verticalScrollBar().width()
        # Also subtract an extra space as a margin to ensure no horizontal scrollbar appears
        extra_margin = self.style().pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)

        # Adjust `3` if you need a different number of thumbnails per row.
        available_width = (
            self.scroll_area.viewport().width()
            - self.scroll_layout.horizontalSpacing() * 4
            - scrollbar_width
            - extra_margin
        ) // 3
        return available_width

    def find_thumbnails(self, word_dir):
        """Find all image files in the word directory."""
        thumbnails = []
        for root, dirs, files in os.walk(word_dir):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(root, file))
        return thumbnails

    def get_aspect_ratio(self, size: QSize) -> float:
        return size.width() / size.height()

    def find_first_thumbnail(self, word_dir):
        """Find the first image in the word directory, used as a thumbnail."""
        for root, dirs, files in os.walk(word_dir):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    return os.path.join(root, file)
        return None

    def show_variations(self, base_word):
        # Placeholder for expanding variations view
        print(f"Show variations for {base_word}")

    def reload_dictionary_tab(self):
        self.load_base_words()
