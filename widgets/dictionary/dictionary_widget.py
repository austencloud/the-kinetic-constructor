import os
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QSize, QCoreApplication
from path_helpers import get_images_and_data_path
from widgets.dictionary.dictionary_variation_manager import DictionaryVariationManager

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame,
)


class DictionaryWidget(QWidget):
    def __init__(self, main_widget):
        super().__init__()
        self.main_widget = main_widget
        self.setup_ui()
        self.variation_manager = DictionaryVariationManager(self)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Scroll area for base words (thumbnails)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setHorizontalSpacing(
            20
        )  # Set horizontal spacing between thumbnails
        self.scroll_layout.setVerticalSpacing(
            20
        )  # Set vertical spacing between thumbnails
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

        # Load and display base words as thumbnails
        self.load_base_words()

    def load_base_words(self):
        dictionary_dir = get_images_and_data_path("dictionary")
        if not os.path.exists(dictionary_dir):
            os.makedirs(dictionary_dir)
        base_words = [
            d
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d))
        ]

        # Get screen size
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        screen_height = screen_size.height()
        thumbnail_height = max(
            screen_height // 8, 100
        ) 

        for i, word in enumerate(base_words):
            thumbnail = self.find_first_thumbnail(os.path.join(dictionary_dir, word))
            if thumbnail:
                pixmap = QPixmap(thumbnail)
                thumbnail_aspect_ratio = self.get_aspect_ratio(pixmap.size())

                # Set the thumbnail size dynamically based on screen size
                thumbnail_size = QSize(
                    int(thumbnail_height * thumbnail_aspect_ratio), thumbnail_height
                )

                label = QLabel()
                label.setPixmap(
                    pixmap.scaled(
                        thumbnail_size,
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
                label.setStyleSheet("border: 1px solid black; margin: 10px;")
                label.mousePressEvent = lambda event, w=word: self.show_variations(w)
                self.scroll_layout.addWidget(label, i // 3, i % 3)
            else:
                # Fallback if no thumbnail is found
                button = QPushButton(word)
                button.clicked.connect(lambda _, w=word: self.show_variations(w))
                self.scroll_layout.addWidget(button, i // 3, i % 3)

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
