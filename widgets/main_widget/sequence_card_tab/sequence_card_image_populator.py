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

        # Get the layout from the current page
        page_layout = self.sequence_card_tab.pages[self.current_page_index].layout()

        # Add the image label to the current page layout
        page_layout.addWidget(image_label, self.current_row, self.current_col)
        self.current_col += 1
        if self.current_col >= max_images_per_row:
            self.current_col = 0
            self.current_row += 1

        # If this was the last image added, add a bottom spacer
        if self.is_last_image_in_page(selected_length):
            self.add_bottom_spacer(page_layout, scaled_pixmap.height())


    def is_current_page_full(self, selected_length: int, image_height: int) -> bool:
        if self.current_page_index == -1:
            return True

        num_rows_per_length = {
            4: 8,
            8: 5,
            16: 3,
        }

        num_rows = num_rows_per_length.get(selected_length, 4)
        total_used_height = (self.current_row + 1) * image_height
        max_height = num_rows * image_height
        return total_used_height + image_height > max_height

    def create_new_page(self):
        self.current_page_index += 1
        new_page_layout = self.sequence_card_tab.page_factory.create_page()
        self.sequence_card_tab.pages.append(new_page_layout)
        self.current_row = 0
        self.current_col = 0

    def is_last_image_in_page(self, selected_length: int) -> bool:
        num_rows = {
            4: 8,
            8: 5,
            16: 3,
        }.get(selected_length, 4)
        total_possible_rows = self.current_row + 1
        return total_possible_rows >= num_rows

    def add_bottom_spacer(self, page_layout: QGridLayout, pixmap_height: int):
        """Adds a bottom spacer row to ensure the last row of images aligns with the top."""
        # Calculate the remaining space
        total_height = self.sequence_card_tab.page_height
        used_height = self.current_row * pixmap_height

        remaining_height = total_height - used_height

        # Add a spacer widget with the remaining height
        if remaining_height > 0:
            spacer = QLabel(self.sequence_card_tab)
            spacer.setFixedHeight(remaining_height)
            spacer.setStyleSheet("background-color: transparent;")
            page_layout.addWidget(
                spacer, self.current_row + 1, 0, 1, self.max_images_per_row
            )
