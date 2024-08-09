from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab


class SequenceCardImageDisplayer:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.main_widget = sequence_card_tab.main_widget
        self.nav_sidebar = sequence_card_tab.nav_sidebar
        self.populator = sequence_card_tab.populator

    def display_images(self, images: list[str]):
        self.pages = self.sequence_card_tab.pages
        self.pages_cache = self.sequence_card_tab.pages_cache
        filtered_images = [
            img_path
            for img_path in images
            if self.get_sequence_length(img_path) == self.nav_sidebar.selected_length
        ]
        sorted_images = sorted(
            filtered_images, key=lambda img_path: self.get_sequence_length(img_path)
        )

        total_width = self.main_widget.width()
        self.margin = total_width // 50
        self.page_width = (
            (total_width // 2) - (2 * self.margin) - (self.nav_sidebar.width() // 2)
        )
        self.page_height = int(self.page_width * 11 / 8.5)
        self.image_card_margin = self.page_width // 40

        self.populator.current_page_index = -1

        for image_path in sorted_images:
            pixmap = QPixmap(image_path)

            max_image_width = self.page_width // 2 - self.image_card_margin
            scale_factor = max_image_width / pixmap.width()
            scaled_height = int(pixmap.height() * scale_factor)

            if scaled_height + self.margin * 2 > self.page_height // 3:
                num_rows = self.get_num_rows_based_on_sequence_length(
                    self.nav_sidebar.selected_length
                )
                scaled_height = int(self.page_height // num_rows - self.margin * 2)
                scale_factor = scaled_height / pixmap.height()
                max_image_width = int(
                    pixmap.width() * scale_factor - self.image_card_margin
                )

            scaled_pixmap = pixmap.scaled(
                max_image_width,
                scaled_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            label = QLabel(self.sequence_card_tab)
            label.setPixmap(scaled_pixmap)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.populator.add_image_to_page(
                label,
                self.nav_sidebar.selected_length,
                scaled_pixmap,
                max_images_per_row=2,
            )

        self.pages_cache[self.nav_sidebar.selected_length] = self.pages.copy()

    def get_sequence_length(self, image_path: str) -> int:
        return self.main_widget.metadata_extractor.get_sequence_length(image_path)

    def get_num_rows_based_on_sequence_length(self, sequence_length: int) -> int:
        num_rows_per_length = {
            4: 7,
            8: 5,
            16: 2,
        }
        return num_rows_per_length.get(sequence_length, 4)
