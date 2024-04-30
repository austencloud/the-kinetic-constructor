from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter
from background_manager import BackgroundManager
from widgets.dictionary_widget.dictionary_browser import DictionaryBrowser
from widgets.dictionary_widget.preview_area import DictionaryPreviewArea
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox
from widgets.dictionary_widget.thumbnail_box.thumbnail_click_handler import (
    ThumbnailClickHandler,
)
from .dictionary_variation_manager import DictionaryVariationManager
from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox

from widgets.dictionary_widget.dictionary_sequence_populator import (
    DictionarySequencePopulator,
)

from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class DictionarySelectionHandler:
    def __init__(self, dictionary_widget: "DictionaryWidget"):
        self.dictionary_widget = dictionary_widget
        self.currently_selected_thumbnail: ThumbnailBox = None

    def update_selection(self, thumbnail_box):
        if self.currently_selected_thumbnail:
            self.currently_selected_thumbnail.set_selected(False)
        self.currently_selected_thumbnail = thumbnail_box
        self.currently_selected_thumbnail.set_selected(True)


class DictionaryWidget(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget

        self._setup_ui()
        self.selected_sequence_dict = None

    def _setup_ui(self):
        self._setup_components()
        self._setup_layout()
        self._setup_background()

    def _setup_background(self):
        self.background_manager = BackgroundManager(self)

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.dictionary_browser, 5)
        self.layout.addWidget(self.preview_area, 3)
        self.setLayout(self.layout)

    def _setup_components(self):
        # Setup handlers
        self.selection_handler = DictionarySelectionHandler(self)
        self.thumbnail_click_handler = ThumbnailClickHandler(self)
        self.variation_manager = DictionaryVariationManager(self)
        self.sequence_populator = DictionarySequencePopulator(self)
        # Setup areas
        self.dictionary_browser = DictionaryBrowser(self)
        self.preview_area = DictionaryPreviewArea(self)

    def reload_dictionary_tab(self):
        self.dictionary_browser.load_base_words()  # Call load_base_words to refresh the UI

    def paintEvent(self, event):
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)
