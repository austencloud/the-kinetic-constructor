from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QResizeEvent
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication

from main_window.main_widget.dictionary_widget.dictionary_browser.dictionary_browser import (
    DictionaryBrowser,
)
from main_window.main_widget.dictionary_widget.dictionary_deletion_handler import (
    DictionaryDeletionHandler,
)
from .dictionary_selection_handler import DictionarySelectionHandler
from .dictionary_preview_area import DictionaryPreviewArea
from .dictionary_sequence_populator import DictionarySequencePopulator

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class DictionaryWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.indicator_label = (
            main_widget.top_builder_widget.sequence_widget.indicator_label
        )
        self.selected_sequence_dict = None

        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.dictionary_settings = (
            self.main_widget.main_window.settings_manager.dictionary_settings
        )
        self._setup_ui()
        self.connect_signals()
        self.initialized = False
        self.background_manager = None

    def connect_signals(self):
        self.main_widget.main_window.settings_manager.background_changed.connect(
            self.update_background_manager
        )

    def update_background_manager(self, bg_type: str):
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.update()

    def _setup_ui(self) -> None:
        self._setup_handlers()
        self.browser = DictionaryBrowser(self)
        self.preview_area = DictionaryPreviewArea(self)
        self._setup_layout()

    def _setup_handlers(self) -> None:
        self.deletion_handler = DictionaryDeletionHandler(self)
        self.selection_handler = DictionarySelectionHandler(self)
        self.sequence_populator = DictionarySequencePopulator(self)

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addWidget(self.browser, 5)
        self.setLayout(self.layout)

    def paintEvent(self, event) -> None:
        if self.background_manager is None:
            self.background_manager = self.global_settings.setup_background_manager(
                self
            )
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)

    def resize_dictionary_widget(self) -> None:
        self.browser.resize_dictionary_browser()
        self.preview_area.resize_preview_area()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.preview_area.resize_preview_area()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(100, self.show_initial_section)

    def show_initial_section(self):
        current_section = (
            self.browser.dictionary_widget.dictionary_settings.get_current_section()
        )
        initial_selection_widget = self.browser.initial_selection_widget
        section_map = {
            "filter_choice": initial_selection_widget.show_filter_choice_widget,
            "starting_letter": initial_selection_widget.show_starting_letter_section,
            "contains_letters": initial_selection_widget.show_contains_letter_section,
            "sequence_length": initial_selection_widget.show_length_section,
            "level": initial_selection_widget.show_level_section,
            "starting_position": initial_selection_widget.show_starting_position_section,
            "author": initial_selection_widget.show_author_section,
            "browser": self.browser.show_browser_with_filters_from_settings,
        }

        if current_section in section_map:
            section_map[current_section]()
