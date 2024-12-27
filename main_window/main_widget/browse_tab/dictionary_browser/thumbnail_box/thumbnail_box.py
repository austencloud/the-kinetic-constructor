from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication
from main_window.main_widget.browse_tab.dictionary_browser.thumbnail_box.thumbnail_box_nav_btns import (
    ThumbnailBoxNavButtonsWidget,
)
from .word_label import WordLabel
from .thumbnail_image_label import ThumbnailImageLabel
from .variation_number_label import VariationNumberLabel

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.dictionary_browser.dictionary_browser import (
        DictionaryBrowser,
    )


class ThumbnailBox(QWidget):
    def __init__(self, browser: "DictionaryBrowser", word: str, thumbnails) -> None:
        super().__init__(browser)
        self.margin = 10
        self.word = word
        self.thumbnails: list[str] = thumbnails
        self.browser = browser
        self.main_widget = browser.dictionary.main_widget
        self.initial_size_set = False
        self.current_index = 0
        self.browser = browser
        self.setContentsMargins(0, 0, 0, 0)
        self.favorite_status = False  # Default favorite status
        self._setup_components()
        self._setup_layout()
        self.layout.setSpacing(0)
        self.load_favorite_status()
        self.word_label.update_favorite_icon(self.favorite_status)

    def _setup_components(self):
        self.word_label = WordLabel(self)
        self.image_label = ThumbnailImageLabel(self)
        self.variation_number_label = VariationNumberLabel(self)
        self.nav_buttons_widget = ThumbnailBoxNavButtonsWidget(self)

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addStretch()
        self.layout.addWidget(self.word_label)
        self.layout.addWidget(self.variation_number_label)
        self.layout.addWidget(
            self.image_label,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        self.layout.addWidget(self.nav_buttons_widget)
        self.layout.addStretch()
        self.layout.setContentsMargins(
            self.margin, self.margin, self.margin, self.margin
        )
        # self.setStyleSheet("background-color: rgba(255, 255, 255, 0.5);")

    def is_favorite(self) -> bool:
        return self.favorite_status

    def toggle_favorite_status(self):
        self.favorite_status = not self.favorite_status
        self.word_label.update_favorite_icon(self.favorite_status)
        QApplication.processEvents()
        self.save_favorite_status()

        current_filter = (
            self.browser.dictionary.dictionary_settings.get_current_filter()
        )
        if current_filter and current_filter.get("favorites"):
            if not self.favorite_status:
                self.hide()
            else:
                self.show()

    def load_favorite_status(self):
        # Load favorite status from metadata
        if self.thumbnails:
            first_thumbnail = self.thumbnails[0]
            self.favorite_status = (
                self.main_widget.metadata_extractor.get_favorite_status(first_thumbnail)
            )

    def save_favorite_status(self):
        # Save favorite status to metadata
        for thumbnail in self.thumbnails:
            self.main_widget.metadata_extractor.set_favorite_status(
                thumbnail, self.favorite_status
            )

    def resize_thumbnail_box(self):
        scrollbar_width = (
            self.browser.scroll_widget.scroll_area.verticalScrollBar().width()
        )
        parent_width = self.browser.scroll_widget.width() - scrollbar_width

        width = parent_width // 3
        self.setFixedWidth(width)
        self.image_label.update_thumbnail(self.current_index)
        self.word_label.resize_word_label()
        self.resize_variation_number_label()

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        self.nav_buttons_widget.thumbnails = thumbnails
        if self == self.browser.dictionary.preview_area.current_thumbnail_box:
            self.browser.dictionary.preview_area.update_thumbnails(self.thumbnails)
        self.image_label.thumbnails = thumbnails
        self.image_label.set_pixmap_to_fit(QPixmap(self.thumbnails[self.current_index]))
        if len(self.thumbnails) == 1:
            self.variation_number_label.hide()
        else:
            self.variation_number_label.update_index(self.current_index + 1)

    def refresh_ui(self):
        self.update_thumbnails(self.thumbnails)

    def resize_variation_number_label(self):
        font = self.font()
        font.setPointSize(self.width() // 35)
        font.setBold(True)
        self.variation_number_label.setFont(font)
