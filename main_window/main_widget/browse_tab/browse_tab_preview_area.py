from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from .browse_tab_preview_area_image_label import BrowseTabPreviewAreaImageLabel
from .browse_tab_button_panel import BrowseTabButtonPanel
from .thumbnail_box.browse_tab_preview_area_word_label import (
    BrowseTabPreviewAreaWordLabel,
)
from .thumbnail_box.preview_area_nav_btns import PreviewAreaNavButtonsWidget
from .thumbnail_box.thumbnail_box import ThumbnailBox
from .thumbnail_box.variation_number_label import VariationNumberLabel


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class BrowseTabPreviewArea(QWidget):
    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__(browse_tab)
        self.thumbnails = []
        self.current_index = 0
        self.main_widget = browse_tab.main_widget
        self.browse_tab = browse_tab
        self.sequence_json = None
        self.initialized = False
        self.current_thumbnail_box: ThumbnailBox = None
        self._setup_components()
        self._setup_layout()
        self.hide()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.image_label = BrowseTabPreviewAreaImageLabel(self)
        self.nav_buttons_widget = PreviewAreaNavButtonsWidget(self)
        self.word_label = BrowseTabPreviewAreaWordLabel(self)
        self.button_panel = BrowseTabButtonPanel(self)

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

        elif len(self.thumbnails) == 0:
            self.image_label.show_placeholder()
            self.variation_number_label.clear()
            self.word_label.clear()

    def _show_components(self):
        self.word_label.show()
        self.variation_number_label.show()
        self.button_panel.show_buttons()

    def update_preview(self, index):
        if index is None:
            self.image_label.show_placeholder()
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

    def clear_preview(self):
        self.image_label.show_placeholder()
        self.variation_number_label.clear()
        self.word_label.clear()
        self.current_index = 0
        self.current_thumbnail_box = None
        self.thumbnails = []
        self.nav_buttons_widget.hide()
        self.variation_number_label.hide()
        self.initialized = False
