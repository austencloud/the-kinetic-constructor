from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QApplication
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.thumbnail_image_label import (
    ThumbnailImageLabel,
)
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.variation_number_label import (
    VariationNumberLabel,
)
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.word_label import (
    WordLabel,
)
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.thumbnail_box_nav_btns import (
    ThumbnailBoxNavButtonsWidget,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_dictionary_browser import (
        SequenceDictionaryBrowser,
    )


class WriteTabThumbnailBox(QWidget):
    def __init__(
        self, browser: "SequenceDictionaryBrowser", word: str, thumbnails
    ) -> None:
        super().__init__(browser)
        self.margin = 10
        self.word = word
        self.thumbnails: list[str] = thumbnails
        self.browser = browser
        self.main_widget = (
            browser.write_tab.main_widget
        )  # Adjusted to work with WriteTab
        self.initial_size_set = False
        self.current_index = 0
        self.setContentsMargins(0, 0, 0, 0)
        self.favorite_status = False  # Default favorite status
        self._setup_components()
        self._setup_layout()
        self.layout.setSpacing(0)
        self.load_favorite_status()
        self.word_label.update_favorite_icon(self.favorite_status)

    def _setup_components(self):
        self.metadata_extractor = MetaDataExtractor(self.main_widget)
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

    def load_favorite_status(self):
        # This feature may not be needed, so you can simplify it or remove it
        if self.thumbnails:
            first_thumbnail = self.thumbnails[0]
            self.favorite_status = self.metadata_extractor.get_favorite_status(
                first_thumbnail
            )

    def resize_thumbnail_box(self):
        scrollbar_width = self.browser.verticalScrollBar().width()
        parent_width = self.browser.width() - scrollbar_width
        width = parent_width // 3
        self.setFixedWidth(width)
        self.image_label.update_thumbnail(self.current_index)
        self.word_label.resize_base_word_label()
        self.resize_variation_number_label()

    # Other methods can remain unchanged

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        self.nav_buttons_widget.thumbnails = thumbnails
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

    def toggle_favorite_status(self):
        self.favorite_status = not self.favorite_status
        self.word_label.update_favorite_icon(self.favorite_status)
        QApplication.processEvents()
        self.save_favorite_status()


    def load_favorite_status(self):
        # Load favorite status from metadata
        if self.thumbnails:
            first_thumbnail = self.thumbnails[0]
            self.favorite_status = self.metadata_extractor.get_favorite_status(
                first_thumbnail
            )

    def save_favorite_status(self):
        # Save favorite status to metadata
        for thumbnail in self.thumbnails:
            self.metadata_extractor.set_favorite_status(thumbnail, self.favorite_status)
