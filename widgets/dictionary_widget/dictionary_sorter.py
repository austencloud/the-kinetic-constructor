import os
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QComboBox, QApplication

from widgets.path_helpers.path_helpers import get_images_and_data_path
from widgets.dictionary_widget.dictionary_browser.section_header import SectionHeader
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionarySorterWidget(QWidget):
    def __init__(self, browser: "DictionaryBrowser") -> None:
        super().__init__(browser)
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.lowercase_letters = set(["α", "β", "θ"])
        self.setup_ui()

        self.custom_order = [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "Σ",
            "Δ",
            "θ",
            "Ω",
            "W-",
            "X-",
            "Y-",
            "Z-",
            "Σ-",
            "Δ-",
            "θ-",
            "Ω-",
            "Φ",
            "Ψ",
            "Λ",
            "Φ-",
            "Ψ-",
            "Λ-",
            "α",
            "β",
            "Γ",
        ]

    def setup_ui(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.sort_combobox = QComboBox()
        self.sort_combobox.addItems(["Word Length", "Alphabetical"])
        self.sort_combobox.currentTextChanged.connect(self.on_sort_order_changed)
        self.layout.addWidget(self.sort_combobox)

    def on_sort_order_changed(self, sort_order):
        self.sort_and_display_thumbnails(sort_order)
        self.browser.scroll_widget.scroll_area.verticalScrollBar().setValue(0)

    def sort_and_display_thumbnails(self, sort_order="Word Length"):
        self.browser.scroll_widget.clear_layout()
        sections = set()  # Track sections for the sidebar

        base_words = self.get_sorted_base_words(sort_order)
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3

        for word, thumbnails in base_words:
            section = self.get_section_from_word(word, sort_order)
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
        if sort_order == "Word Length":
            sorted_sections = sorted(
                sections, key=lambda x: int(x) if x.isdigit() else x
            )
        else:
            sorted_sections = sorted(sections, key=self.custom_sort_key)

        self.browser.sidebar.update_sidebar(sorted_sections)

    def get_sorted_base_words(self, sort_order):
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (d, self.find_thumbnails(os.path.join(dictionary_dir, d)))
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d)) and "__pycache__" not in d
        ]

        if sort_order == "Word Length":
            base_words.sort(key=lambda x: (len(x[0].replace("-", "")), x[0]))
        else:
            base_words.sort(key=lambda x: x[0])
        return base_words

    def find_thumbnails(self, word_dir: str):
        thumbnails = []
        for root, _, files in os.walk(word_dir):
            if "__pycache__" in root:
                continue
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    thumbnails.append(os.path.join(root, file))
        return thumbnails

    def get_section_from_word(self, word, sort_order):
        if sort_order == "Word Length":
            return str(len(word.replace("-", "")))
        else:
            section = word[:2] if len(word) > 1 and word[1] == "-" else word[0]
            if not section.isdigit():
                if section[0] in self.lowercase_letters:
                    section = section.lower()
                else:
                    section = section.upper()
            return section

    def custom_sort_key(self, section):
        try:
            return self.custom_order.index(section)
        except ValueError:
            return len(self.custom_order)  # put unknown sections at the end
