from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSplitter
from background_manager import BackgroundManager
from widgets.dictionary_widget.dictionary_deletion_manager import (
    DictionaryDeletionManager,
)
from .dictionary_browser.dictionary_browser import DictionaryBrowser
from .dictionary_selection_handler import DictionarySelectionHandler
from .dictionary_preview_area import DictionaryPreviewArea
from .dictionary_sequence_populator import DictionarySequencePopulator

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class DictionaryWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget

        self._setup_ui()
        self.selected_sequence_dict = None

    def _setup_ui(self) -> None:
        self.deletion_manager = DictionaryDeletionManager(self)
        self.browser = DictionaryBrowser(self)
        self.preview_area = DictionaryPreviewArea(self)
        self._setup_handlers()
        self._setup_layout()

    def _setup_handlers(self) -> None:
        self.background_manager = BackgroundManager(self)
        self.selection_handler = DictionarySelectionHandler(self)
        self.sequence_populator = DictionarySequencePopulator(self)
        self.background_manager.update_required.connect(self.update)

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.browser, 6)
        self.layout.addWidget(self.preview_area, 3)

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)

    def resize_dictionary_widget(self) -> None:
        self.browser.resize_dictionary_browser()
