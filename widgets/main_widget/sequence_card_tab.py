from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QGridLayout, QFrame
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt, QSize
import os
from typing import TYPE_CHECKING, List
from widgets.path_helpers.path_helpers import get_sequence_card_image_exporter_path
from widgets.sequence_card_image_exporter import SequenceCardImageExporter

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class SequenceCardTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.sequence_card_image_exporter = SequenceCardImageExporter(self)
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Single Scroll Area for sequence cards
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setStyleSheet("background-color: #f0f0f0;")  # Light gray for background
        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)

        # Load and display images
        self.load_images()

    def load_images(self):
        export_path = get_sequence_card_image_exporter_path()
        images = self.get_all_images(export_path)
        self.display_images(images)

    def get_all_images(self, path: str) -> List[str]:
        images = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(root, file))
        return images

    def display_images(self, images: List[str]):
        # Sort images by sequence length using a lambda function that correctly passes the image path
        sorted_images = sorted(images, key=lambda img_path: self.get_sequence_length(img_path))

        page_width = 595  # Approx A4 width in pixels at 72 DPI
        page_height = 842  # Approx A4 height in pixels at 72 DPI
        max_page_width = self.width() * 0.9  # Scale down to fit within the window
        scale_factor = max_page_width / page_width

        scaled_page_width = int(page_width * scale_factor)
        scaled_page_height = int(page_height * scale_factor)
        max_image_width = scaled_page_width // 3  # Max 3 images per row

        # Creating each "page"
        row, col = 0, 0
        current_page = None
        for image_path in sorted_images:
            if col == 0:
                # Create new page
                current_page = QFrame(self.scroll_content)
                current_page.setFixedSize(scaled_page_width, scaled_page_height)
                current_page_layout = QGridLayout(current_page)
                current_page_layout.setContentsMargins(10, 10, 10, 10)
                current_page_layout.setSpacing(10)
                self.scroll_layout.addWidget(current_page)

            # Load and resize image
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                max_image_width,
                max_image_width,  # Assuming square layout
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            label = QLabel(self)
            label.setPixmap(scaled_pixmap)

            # Add to layout on the current page
            current_page_layout.addWidget(label, row, col)

            col += 1
            if col >= 3:  # Max columns
                col = 0
                row += 1

            # Check if we need to start a new "page"
            if row >= 3:  # 3 rows of images max
                row = 0

    def get_sequence_length(self, image_path: str) -> int:
        return self.main_widget.metadata_extractor.get_sequence_length(image_path)
