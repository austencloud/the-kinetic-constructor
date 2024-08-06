from PyQt6.QtWidgets import QLabel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.sequence_card_tab.sequence_card_tab import SequenceCardTab

class SequenceCardImagePopulator:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.current_page_index = -1
        self.current_row = 0
        self.current_col = 0

    def add_image_to_page(self, image_label: QLabel, image_path, max_images_per_row: int):
        if self.current_page_index == -1 or self.current_page_index >= len(self.sequence_card_tab.pages):
            self.create_new_page()
        
        page_layout = self.sequence_card_tab.pages[self.current_page_index]

        image_height = image_label.pixmap().height()
        row_height = image_height + self.sequence_card_tab.margin
        used_height = self.current_row * row_height

        if used_height + row_height <= self.sequence_card_tab.page_height:
            page_layout.addWidget(image_label, self.current_row, self.current_col)
            self.current_col += 1
            if self.current_col >= max_images_per_row:
                self.current_col = 0
                self.current_row += 1
        else:
            self.create_new_page()
            self.add_image_to_page(image_label, image_path, max_images_per_row)

    def create_new_page(self):
        self.current_page_index += 1
        new_page_layout = self.sequence_card_tab.page_factory.create_page()
        self.sequence_card_tab.pages.append(new_page_layout)
        self.current_row = 0
        self.current_col = 0
