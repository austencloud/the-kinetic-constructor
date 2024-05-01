import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QGridLayout,
    QPushButton,
    QStyle,
)
from PyQt6.QtCore import QSize
from path_helpers import get_images_and_data_path
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryBrowser(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget") -> None:
        super().__init__(dictionary_widget)
        self.dictionary_widget = dictionary_widget
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QGridLayout(self.scroll_content)
        self.scroll_layout.setHorizontalSpacing(20)
        self.scroll_layout.setVerticalSpacing(20)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setStyleSheet("background: transparent;")
        self.layout.addWidget(self.scroll_area)

    def load_base_words(self):
        dictionary_dir = get_images_and_data_path("dictionary")
        if not os.path.exists(dictionary_dir):
            os.makedirs(dictionary_dir)
        base_words = [
            d
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d))
        ]

        self.clear_layout(self.scroll_layout)  # Clear existing widgets in the layout

        for i, word in enumerate(base_words):
            thumbnails = self.find_thumbnails(os.path.join(dictionary_dir, word))
            if thumbnails:
                thumbnail_box = ThumbnailBox(self, word, thumbnails)
                self.scroll_layout.addWidget(thumbnail_box, i // 3, i % 3)
            else:
                button = QPushButton(word)
                button.clicked.connect(lambda _, w=word: self.show_variations(w))
                self.scroll_layout.addWidget(button, i // 3, i % 3)

        self.scroll_content.setLayout(self.scroll_layout)
        self.update()

    def thumbnail_area_width(self):
        scrollbar_width = 0
        if self.scroll_area.verticalScrollBar().isVisible():
            scrollbar_width = self.scroll_area.verticalScrollBar().width()
        extra_margin = self.style().pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent)
        available_width = (
            self.scroll_area.viewport().width()
            - self.scroll_layout.horizontalSpacing() * 4
            - scrollbar_width
            - extra_margin
        ) // 3
        return available_width

    def clear_layout(self):
        """Remove all widgets from the layout."""
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())

    def add_thumbnail(self, thumbnail_box, row, col):
        self.scroll_layout.addWidget(thumbnail_box, row, col)

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
        print(f"Show variations for {base_word}")
