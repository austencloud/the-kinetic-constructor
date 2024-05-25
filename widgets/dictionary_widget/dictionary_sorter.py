import os
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox

from path_helpers import get_images_and_data_path
from widgets.dictionary_widget.dictionary_browser.section_header import SectionHeader
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionarySorter(QWidget):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.setup_ui()

    def setup_ui(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.sort_combobox = QComboBox()
        self.sort_combobox.addItems(["Word Length", "Alphabetical"])
        self.sort_combobox.currentTextChanged.connect(self.on_sort_order_changed)
        self.layout.addWidget(self.sort_combobox)

    def on_sort_order_changed(self, sort_order):
        self.sort_and_display_thumbnails(sort_order)

    def sort_and_display_thumbnails(self, sort_order="Word Length"):
        self.browser.scroll_widget.clear_layout()
        sections = set()  # Track sections for the sidebar

        base_words = self.get_sorted_base_words(sort_order)
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3

        for word, thumbnails in base_words:
            section = (
                len(word.replace("-", ""))
                if sort_order == "Word Length"
                else word[0].upper()
            )
            sections.add(section)

            if section != current_section:
                if current_section is not None:
                    row_index += 1

                current_section = section
                header_title = f"{section}"
                header = SectionHeader(header_title, self.browser)
                self.browser.scroll_widget.section_headers[section] = header
                self.browser.scroll_widget.grid_layout.addWidget(
                    header, row_index, 0, 1, num_columns
                )
                row_index += 1
                column_index = 0

            # Add thumbnail boxes
            if word not in self.browser.scroll_widget.thumbnail_boxes_dict:
                thumbnail_box = ThumbnailBox(self.browser, word, thumbnails)
                thumbnail_box.image_label.update_thumbnail()
                self.browser.scroll_widget.thumbnail_boxes_dict[word] = thumbnail_box

            thumbnail_box = self.browser.scroll_widget.thumbnail_boxes_dict[word]
            self.browser.scroll_widget.grid_layout.addWidget(
                thumbnail_box, row_index, column_index
            )
            column_index += 1

            # Check if row is filled
            if column_index == num_columns:
                column_index = 0
                row_index += 1

        # Update the sidebar with sections
        self.browser.sidebar.update_sidebar(sorted(sections))

    def get_sorted_base_words(self, sort_order):
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (d, self.find_thumbnails(os.path.join(dictionary_dir, d)))
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d))
        ]
        if sort_order == "Word Length":
            base_words.sort(key=lambda x: (len(x[0].replace("-", "")), x[0]))
        else:
            base_words.sort(key=lambda x: x[0])
        return base_words

    def find_thumbnails(self, word_dir: str):
        thumbnails = []
        for root, _, files in os.walk(word_dir):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(root, file))
        return thumbnails
