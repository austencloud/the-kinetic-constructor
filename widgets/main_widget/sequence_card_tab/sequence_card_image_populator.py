from PyQt6.QtWidgets import QLabel, QGridLayout
from PyQt6.QtGui import QPixmap
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab


class SequenceCardImagePopulator:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0
        self.max_images_per_row = 2  # Assuming two images per row

    def add_image_to_page(
        self,
        image_label: QLabel,
        selected_length,
        scaled_pixmap: QPixmap,
        max_images_per_row: int,
    ):
        if self.current_page_index == -1 or self.is_current_page_full(
            selected_length, scaled_pixmap.height()
        ):
            self.create_new_page()

        page_layout = self.sequence_card_tab.pages[self.current_page_index]

        # Add the image label to the current page layout
        page_layout.addWidget(image_label, self.current_row, self.current_col)
        self.current_col += 1
        if self.current_col >= max_images_per_row:
            self.current_col = 0
            self.current_row += 1

    def is_current_page_full(self, selected_length: int, image_height: int) -> bool:
        if self.current_page_index == -1:
            return True

        num_rows_per_length = {
            4: 7,
            8: 4,
            12: 3,
            16: 2,
        }

        num_rows = num_rows_per_length.get(selected_length, 4)
        total_used_height = (self.current_row) * image_height
        max_height = num_rows * image_height
        return total_used_height + image_height > max_height

    def create_new_page(self):
        self.current_page_index += 1
        new_page_layout = self.sequence_card_tab.page_factory.create_page()
        self.sequence_card_tab.pages.append(new_page_layout)
        self.current_row = 0
        self.current_col = 0
