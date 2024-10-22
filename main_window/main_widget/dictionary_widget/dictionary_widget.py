from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QResizeEvent
from PyQt6.QtWidgets import QWidget, QHBoxLayout

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
        self.indicator_label = main_widget.sequence_widget.indicator_label
        self.selected_sequence_dict = None

        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.dictionary_settings = (
            self.main_widget.main_window.settings_manager.dictionary_settings
        )
        self._setup_ui()
        self.initialized = False

    def update_background_manager(self, bg_type: str):
        if self.background_manager:
            self.background_manager.stop_animation()
        self.background_manager = self.global_settings.setup_background_manager(self)
        self.background_manager.update_required.connect(self.update)
        self.background_manager.start_animation()
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

    def resize_dictionary_widget(self) -> None:
        self.browser.resize_dictionary_browser()
        self.preview_area.resize_preview_area()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.preview_area.resize_preview_area()

    def show_initial_section(self):
        current_section = (
            self.browser.dictionary_widget.dictionary_settings.get_current_section()
        )
        initial_selection_widget = self.browser.initial_selection_widget

        # Use the generic `show_section` method with the corresponding section names
        section_map = {
            "filter_choice": lambda: initial_selection_widget.show_section(
                "filter_choice"
            ),
            "starting_letter": lambda: initial_selection_widget.show_section(
                "starting_letter"
            ),
            "contains_letters": lambda: initial_selection_widget.show_section(
                "contains_letters"
            ),
            "sequence_length": lambda: initial_selection_widget.show_section(
                "sequence_length"
            ),
            "level": lambda: initial_selection_widget.show_section("level"),
            "starting_position": lambda: initial_selection_widget.show_section(
                "starting_position"
            ),
            "author": lambda: initial_selection_widget.show_section("author"),
            "browser": self.browser.show_browser_with_filters_from_settings,
        }

        if current_section in section_map:
            section_map[current_section]()
