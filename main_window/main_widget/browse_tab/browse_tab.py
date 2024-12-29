from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.browse_tab.sequence_picker.sequence_picker_sort_widget import (
    SequencePickerSortWidget,
)
from main_window.main_widget.browse_tab.sequence_picker.sequence_picker import (
    SequencePicker,
)

from .browse_tab_filter_manager import BrowseTabFilterManager
from .browse_tab_layout_manager import BrowseTabLayoutManager
from .browse_tab_getter import BrowseTabGetter
from .sequence_picker.sequence_picker_filter_selector.sequence_picker_filter_selector import (
    SequencePickerFilterSelector,
)
from .sequence_picker.sequence_picker_nav_sidebar import SequencePickerNavSidebar
from .browse_tab_section_manager import BrowseTabSectionManager
from .browse_tab_thumbnail_box_sorter import BrowseTabThumbnailBoxSorter
from .sequence_picker.sequence_picker_currently_displaying_label import (
    SequencePickerCurrentlyDisplayingLabel,
)
from .sequence_picker.sequence_picker_scroll_widget import SequencePickerScrollWidget
from .sequence_picker.sequence_picker_progress_bar import SequencePickerPirogressBar
from .browse_tab_options_panel import BrowseTabOptionsPanel
from .browse_tab_ui_updater import BrowseTabUIUpdater
from .browse_tab_go_back_button import BrowseTabGoBackButton
from .sequence_picker.sequence_picker_count_label import SequencePickerCountLabel
from .deletion_handler.browse_tab_deletion_handler import BrowseTabDeletionHandler
from .browse_tab_selection_handler import BrowseTabSelectionHandler
from .sequence_viewer import SequenceViewer
from .browse_tab_edit_sequence_handler import BrowseTabEditSequenceHandler

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
        self.browse_tab_settings = (
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

        # Components
        self.sequence_picker = SequencePicker(self)
        self.sequence_viewer = SequenceViewer(self)

        self.go_back_button = BrowseTabGoBackButton(self)

    def show_initial_section(self):
        current_section = self.browse_tab_settings.get_current_section()
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
