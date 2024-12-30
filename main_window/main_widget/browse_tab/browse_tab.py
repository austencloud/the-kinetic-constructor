from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from main_window.main_widget.browse_tab.sequence_picker.sequence_picker_filter_selector.sequence_picker_filter_selector import SequencePickerFilterSelector
from .sequence_picker.sequence_picker import SequencePicker
from .browse_tab_filter_manager import BrowseTabFilterManager
from .browse_tab_getter import BrowseTabGetter
from .browse_tab_section_manager import BrowseTabSectionManager
from .browse_tab_thumbnail_box_sorter import BrowseTabThumbnailBoxSorter
from .browse_tab_ui_updater import BrowseTabUIUpdater
from .deletion_handler.browse_tab_deletion_handler import BrowseTabDeletionHandler
from .browse_tab_selection_handler import BrowseTabSelectionHandler
from .sequence_viewer.sequence_viewer import SequenceViewer
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

    def _setup_ui(self) -> None:
        # Managers
        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionHandler(self)
        self.edit_sequence_handler = BrowseTabEditSequenceHandler(self)
        self.filter_manager = BrowseTabFilterManager(self)
        self.get = BrowseTabGetter(self)
        self.thumbnail_box_sorter = BrowseTabThumbnailBoxSorter(self)
        self.section_manager = BrowseTabSectionManager(self)
        self.ui_updater = BrowseTabUIUpdater(self)

        # Components
        self.sequence_picker = SequencePicker(self)
        self.sequence_viewer = SequenceViewer(self)


    def show_initial_section(self):
        current_section = self.browse_tab_settings.get_current_section()
        selector = self.sequence_picker.filter_selector
        if current_section == "sequence_picker":
            self.filter_manager.show_browser_with_filters_from_settings()
        else:
            selector.show_section(current_section)
