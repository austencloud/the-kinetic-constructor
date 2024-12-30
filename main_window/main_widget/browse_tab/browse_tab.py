from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget

from .sequence_picker.sequence_picker import SequencePicker
from .browse_tab_filter_manager import BrowseTabFilterManager
from .browse_tab_getter import BrowseTabGetter
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
        self.settings = self.main_widget.main_window.settings_manager.browse_settings

        # Components
        self.sequence_picker = SequencePicker(self)
        self.sequence_viewer = SequenceViewer(self)

        # Managers
        self.deletion_handler = BrowseTabDeletionHandler(self)
        self.selection_handler = BrowseTabSelectionHandler(self)
        self.edit_sequence_handler = BrowseTabEditSequenceHandler(self)
        self.filter_manager = BrowseTabFilterManager(self)
        self.get = BrowseTabGetter(self)
        self.ui_updater = BrowseTabUIUpdater(self)