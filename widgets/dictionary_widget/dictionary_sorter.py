import os
import json
from datetime import datetime
from typing import TYPE_CHECKING
from PIL import Image
from widgets.dictionary_widget.dictionary_browser.section_header import SectionHeader
from widgets.dictionary_widget.thumbnail_box.metadata_extractor import MetaDataExtractor
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
from widgets.path_helpers.path_helpers import get_images_and_data_path
from .sorting_order import sorting_order, lowercase_letters

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class DictionarySorter:
    def __init__(self, browser: "DictionaryBrowser") -> None:
        self.browser = browser
        self.metadata_extractor = browser.main_widget.metadata_extractor

    def sort_and_display_thumbnails(self, sort_order="Sequence Length"):
        self.browser.scroll_widget.clear_layout()
        sections = {}

        base_words = self.get_sorted_base_words(sort_order)
        current_section = None
        row_index = 0
        column_index = 0
        num_columns = 3

        for word, thumbnails, seq_length in base_words:
            # Pass thumbnails correctly
            section = self.get_section_from_word(
                word, sort_order, seq_length, thumbnails
            )

            if section not in sections:
                sections[section] = []

            sections[section].append((word, thumbnails))

        sorted_sections = self._get_sorted_sections(sort_order, sections.keys())
        self.browser.sidebar.update_sidebar(sorted_sections, sort_order)

        for section in sorted_sections:
            if sort_order == "Date Added":
                if section == "Unknown":
                    continue

                day, month, year = section.split("-")
                formatted_day = f"{int(day)}-{int(month)}"

                if year != current_section:
                    row_index += 1
                    self._add_header(row_index, num_columns, year)
                    row_index += 1
                    current_section = year

                row_index += 1
                self._add_header(row_index, num_columns, formatted_day)
                row_index += 1
            else:
                row_index += 1
                self._add_header(row_index, num_columns, section)
                row_index += 1

            column_index = 0

            for word, thumbnails in sections[section]:
                self._add_thumbnail_box(row_index, column_index, word, thumbnails)
                column_index += 1
                if column_index == num_columns:
                    column_index = 0
                    row_index += 1

    def _add_header(self, row_index, num_columns, section):
        header_title = f"{section}"
        header = SectionHeader(header_title, self.browser)
        self.browser.scroll_widget.section_headers[section] = header
        self.browser.scroll_widget.grid_layout.addWidget(
            header, row_index, 0, 1, num_columns
        )

    def _add_thumbnail_box(self, row_index, column_index, word, thumbnails):
        if word not in self.browser.scroll_widget.thumbnail_boxes_dict:
            thumbnail_box = ThumbnailBox(self.browser, word, thumbnails)
            thumbnail_box.image_label.update_thumbnail()
            self.browser.scroll_widget.thumbnail_boxes_dict[word] = thumbnail_box

        thumbnail_box = self.browser.scroll_widget.thumbnail_boxes_dict[word]
        self.browser.scroll_widget.grid_layout.addWidget(
            thumbnail_box, row_index, column_index
        )

    def _get_sorted_sections(self, sort_order, sections):
        if sort_order == "Sequence Length":
            sorted_sections = sorted(
                sections, key=lambda x: int(x) if x.isdigit() else x
            )
        elif sort_order == "Date Added":
            sorted_sections = sorted(
                [s for s in sections if s != "Unknown"],
                key=lambda x: datetime.strptime(x, "%m-%d-%Y"),
                reverse=True,
            )
            if "Unknown" in sections:
                sorted_sections.append("Unknown")
        else:
            sorted_sections = sorted(sections, key=self.custom_sort_key)
        return sorted_sections

    def get_sorted_base_words(self, sort_order):
        dictionary_dir = get_images_and_data_path("dictionary")
        base_words = [
            (d, self.find_thumbnails(os.path.join(dictionary_dir, d)), None)
            for d in os.listdir(dictionary_dir)
            if os.path.isdir(os.path.join(dictionary_dir, d)) and "__pycache__" not in d
        ]

        for i, (word, thumbnails, _) in enumerate(base_words):
            sequence_length = self.get_sequence_length_from_thumbnails(thumbnails)
            base_words[i] = (word, thumbnails, sequence_length)

        if sort_order == "Sequence Length":
            base_words.sort(key=lambda x: x[2] if x[2] is not None else float("inf"))
        elif sort_order == "Date Added":
            base_words.sort(key=lambda x: self.get_date_added(x[1]), reverse=True)
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

    def get_section_from_word(
        self, word, sort_order, sequence_length=None, thumbnails=None
    ):
        if sort_order == "Sequence Length":
            return str(sequence_length) if sequence_length is not None else "Unknown"
        elif sort_order == "Date Added":
            if thumbnails:
                date_added = self.get_date_added(thumbnails)
                return date_added.strftime("%m-%d-%Y") if date_added else "Unknown"
            return "Unknown"
        else:
            section = word[:2] if len(word) > 1 and word[1] == "-" else word[0]
            if not section.isdigit():
                if section[0] in lowercase_letters:
                    section = section.lower()
                else:
                    section = section.upper()
            return section

    def custom_sort_key(self, section):
        try:
            return sorting_order.index(section)
        except ValueError:
            return len(sorting_order)  # put unknown sections at the end

    def get_date_added(self, thumbnails):
        dates = []
        for thumbnail in thumbnails:
            image = Image.open(thumbnail)
            info = image.info
            metadata = info.get("metadata")
            if metadata:
                metadata_dict = json.loads(metadata)
                date_added = metadata_dict.get("date_added")
                if date_added:
                    dates.append(datetime.fromisoformat(date_added))
        return max(dates, default=None)

    def get_sequence_length_from_thumbnails(self, thumbnails):
        """Extract the sequence length from the first available thumbnail metadata."""
        for thumbnail in thumbnails:
            length = self.metadata_extractor.get_sequence_length(thumbnail)
            if length:
                return length
        return None
