from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from PyQt6.QtGui import QPixmap
from dictionary.preview_area_image_label import PreviewAreaImageLabel
from widgets.dictionary_widget.dictionary_button_panel import DictionaryButtonPanel
from widgets.dictionary_widget.thumbnail_box.dictionary_preview_area_base_word_label import (
    DictionaryPreviewAreaWordLabel,
)
from widgets.dictionary_widget.thumbnail_box.preview_area_nav_btns import (
    PreviewAreaNavButtonsWidget,
)
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

from widgets.dictionary_widget.thumbnail_box.variation_number_label import (
    VariationNumberLabel,
)

if TYPE_CHECKING:
    from widgets.dictionary_widget.dictionary_widget import DictionaryWidget


class DictionaryPreviewArea(QWidget):
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        super().__init__(dictionary_widget)
        self.thumbnails = []
        self.current_index = 0
        self.main_widget = dictionary_widget.main_widget
        self.dictionary_widget = dictionary_widget
        self.sequence_json = None
        self.initialized = False
        self.current_thumbnail_box: ThumbnailBox = None
        self._setup_components()
        self._hide_components()
        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.word_label)
        layout.addWidget(self.variation_number_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.nav_buttons_widget)
        layout.addWidget(self.button_panel)
        layout.addStretch(1)
        self.setLayout(layout)

    def get_thumbnail_at_current_index(self):
        if self.thumbnails:
            return self.thumbnails[self.current_index]
        return None

    def _setup_components(self):
        self.variation_number_label = VariationNumberLabel(self)
        self.image_label = PreviewAreaImageLabel(self)
        self.nav_buttons_widget = PreviewAreaNavButtonsWidget(self)
        self.word_label = DictionaryPreviewAreaWordLabel(self)
        self.button_panel = DictionaryButtonPanel(self)

    def update_thumbnails(self, thumbnails=[]):
        self.thumbnails = thumbnails
        if self.current_index >= len(self.thumbnails):
            self.current_index = len(self.thumbnails) - 1

        if not self.initialized:
            self._show_components()
            self.initialized = True

        self.update_preview(self.current_index)

        if len(self.thumbnails) > 1:
            self.nav_buttons_widget.show()
            self.variation_number_label.show()

        elif len(self.thumbnails) == 1:
            self.nav_buttons_widget.hide()
            self.current_thumbnail_box.nav_buttons_widget.hide()
            self.variation_number_label.hide()

    def _show_components(self):
        self.word_label.show()
        self.variation_number_label.show()
        self.button_panel.show_buttons()

    def _hide_components(self):
        self.word_label.hide()
        self.variation_number_label.hide()
        self.button_panel.hide_buttons()
        self.update_preview(None)

    def update_preview(self, index):
        if index is None:
            self.image_label.show_placeholder()
            self.image_label.adjust_label_height_for_text()
            self.variation_number_label.clear()
            return

        if self.thumbnails and index is not None:
            pixmap = QPixmap(self.thumbnails[index])
            if pixmap.height() != 0:
                self.image_label.scale_pixmap_to_label(pixmap)

            if self.current_thumbnail_box:
                metadata_extractor = (
                    self.current_thumbnail_box.main_widget.metadata_extractor
                )
                self.sequence_json = metadata_extractor.extract_metadata_from_file(
                    self.thumbnails[index]
                )

    def select_thumbnail(self, thumbnail_box, index, word):
        self.current_index = index
        self.current_thumbnail_box = thumbnail_box
        self.variation_number_label.update_index(index)
        self.word_label.update_word_label(word)
        self.update_thumbnails(self.thumbnails)
        self.update_nav_buttons()
        self.update_preview(index)

    def update_nav_buttons(self):
        self.nav_buttons_widget.current_index = self.current_index
        self.nav_buttons_widget.refresh()

    def showEvent(self, event):
        super().showEvent(event)
        if self.thumbnails and self.current_index is not None:
            self.update_preview(self.current_index)
        else:
            self.image_label.adjust_label_height_for_text()
        self.word_label.resize_word_label()
        self.image_label.show_placeholder()
