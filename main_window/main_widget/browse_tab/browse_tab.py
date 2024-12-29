from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from .browse_tab_filter_manager import BrowseTabFilterManager
from .browse_tab_layout_manager import BrowseTabLayoutManager
from .browse_tab_getter import BrowseTabGetter
from .initial_filter_selection_widget.browse_tab_initial_selections_widget import (
    BrowseTabInitialSelectionsWidget,
)
from .browse_tab_nav_sidebar import BrowseTabNavSidebar
from .browse_tab_section_manager import BrowseTabSectionManager
from .browse_tab_thumbnail_box_sorter import BrowseTabThumbnailBoxSorter
from .browse_tab_currently_displaying_label import BrowseTabCurrentlyDisplayingLabel
from .browse_tab_scroll_widget import BrowseTabScrollWidget
from .browse_tab_progress_bar import BrowseTabProgressBar
from .browse_tab_options_panel import BrowseTabOptionsPanel
from .browse_tab_ui_updater import BrowseTabUIUpdater
from .browse_tab_go_back_button import BrowseTabGoBackButton
from .browse_tab_sequence_count_label import BrowseTabSequenceCountLabel
from .deletion_handler.browse_tab_deletion_handler import BrowseTabDeletionHandler
from .browse_tab_selection_handler import BrowseTabSelectionHandler
from .browse_tab_preview_area import BrowseTabPreviewArea
from .dictionary_sequence_populator import BrowseTabEditSequenceHandler

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BrowseTab(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.indicator_label = main_widget.sequence_widget.indicator_label
        self.selected_sequence_dict = None
        self.currently_displayed_sequences = []

        self.global_settings = (
            self.main_widget.main_window.settings_manager.global_settings
        )
        self.dictionary_settings = (
            self.main_widget.main_window.settings_manager.browse_tab_settings
        )
        self._setup_ui()
        self.initialized = False
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}
        self.layout_manager.setup_layout()

    def _setup_ui(self) -> None:
        # Managers
        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionHandler(self)
        self.edit_sequence_handler = BrowseTabEditSequenceHandler(self)
        self.layout_manager = BrowseTabLayoutManager(self)
        self.filter_manager = BrowseTabFilterManager(self)
        self.get = BrowseTabGetter(self)
        self.thumbnail_box_sorter = BrowseTabThumbnailBoxSorter(self)
        self.section_manager = BrowseTabSectionManager(self)
        self.ui_updater = BrowseTabUIUpdater(self)
        self.currently_displaying_label = BrowseTabCurrentlyDisplayingLabel(self)
        self.sequence_count_label = BrowseTabSequenceCountLabel(self)
        self.progress_bar = BrowseTabProgressBar(self)
        self.options_widget = BrowseTabOptionsPanel(self)
        self.go_back_button = BrowseTabGoBackButton(self)

        # Components
        self.scroll_widget = BrowseTabScrollWidget(self)
        self.nav_sidebar = BrowseTabNavSidebar(self)
        self.preview_area = BrowseTabPreviewArea(self)
        self.initial_selection_widget = BrowseTabInitialSelectionsWidget(self)

    def show_initial_section(self):
        current_section = self.dictionary_settings.get_current_section()
        initial_selection_widget = self.initial_selection_widget

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
            "browser": self.filter_manager.show_browser_with_filters_from_settings,
        }

        if current_section in section_map:
            section_map[current_section]()
