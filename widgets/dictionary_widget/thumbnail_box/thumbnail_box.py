from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShowEvent, QResizeEvent
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from widgets.dictionary_widget.thumbnail_box.metadata_extractor import MetaDataExtractor
from .base_word_label import BaseWordLabel
from .thumbnail_box_nav_buttons_widget import ThumbnailBoxNavButtonsWidget
from .thumbnail_image_label import ThumbnailImageLabel
from .variation_number_label import VariationNumberLabel

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class ThumbnailBox(QWidget):
    def __init__(self, browser: "DictionaryBrowser", base_word, thumbnails) -> None:
        super().__init__(browser)

        self.base_word = base_word
        self.thumbnails = thumbnails
        self.browser = browser
        self.main_widget = browser.dictionary_widget.main_widget
        self.initial_size_set = False
        self.current_index = 0
        self.browser = browser
        self.setContentsMargins(0, 0, 0, 0)
        self._setup_components()
        self._setup_layout()
        self.layout.setSpacing(0)

    def _setup_components(self):
        self.metadata_extractor = MetaDataExtractor(self)
        self.base_word_label = BaseWordLabel(self.base_word)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self.current_index)
        self.nav_buttons_widget = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.base_word_label, 1)
        self.layout.addWidget(self.variation_number_label, 1)
        self.layout.addWidget(
            self.image_label,
            16,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(self.nav_buttons_widget, 1)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

    def resize_thumbnail_box(self):
        scrollbar_width = (
            self.browser.scroll_widget.scroll_area.verticalScrollBar().isVisible()
            * self.browser.scroll_widget.scroll_area.verticalScrollBar().width()
        )
        parent_width = self.browser.width() - scrollbar_width

        width = parent_width // 3
        self.setMinimumWidth(width)
        self.setMaximumWidth(width)

        # self.setMaximumHeight(width)
        self.image_label.update_thumbnail()
