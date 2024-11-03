from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from .go_back_button import GoBackToFilterChoiceButton
from .sequence_count_label import SequenceCountLabel
from .dictionary_browser_resizer import DictionaryBrowserResizer
from .dictionary_filter_manager import DictionaryFilterManager
from .dictionary_progress_bar import DictionaryProgressBar
from .dictionary_browser_getter import DictionaryBrowserGetter
from .dictionary_ui_updater import DictionaryUIUpdater
from .dictionary_browser_layout_manager import DictionaryBrowserLayoutManager
from .initial_filter_selection_widget.dictionary_initial_selections_widget import (
    DictionaryInitialSelectionsWidget,
)
from .currently_displaying_indicator_label import CurrentlyDisplayingIndicatorLabel
from .dictionary_browser_nav_sidebar import DictionaryBrowserNavSidebar
from .dictionary_browser_section_manager import SectionManager
from .thumbnail_box_sorter import ThumbnailBoxSorter
from .dictionary_browser_scroll_widget import DictionaryBrowserScrollWidget
from .dictionary_browser_options_panel.dictionary_browser_options_panel import (
    DictionaryOptionsPanel,
)

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_widget import (
        DictionaryWidget,
    )


class DictionaryBrowser(QWidget):
    def __init__(self, dictioanry: "DictionaryWidget") -> None:
        super().__init__(dictioanry)
        self.dictionary = dictioanry
        self.main_widget = dictioanry.main_widget
        self.initialized = False
        self.currently_displayed_sequences = []
        self.sections: dict[str, list[tuple[str, list[str]]]] = {}

        self._setup_labels()
        self._setup_managers()
        self._setup_components()
        self.layout_manager.setup_layout()

    def _setup_managers(self):
        self.filter_manager = DictionaryFilterManager(self)
        self.get = DictionaryBrowserGetter(self)
        self.ui_updater = DictionaryUIUpdater(self)
        self.section_manager = SectionManager(self)
        self.thumbnail_box_sorter = ThumbnailBoxSorter(self)
        self.layout_manager = DictionaryBrowserLayoutManager(self)

    def _setup_components(self):
        self.nav_sidebar = DictionaryBrowserNavSidebar(self)
        self.scroll_widget = DictionaryBrowserScrollWidget(self)
        self.options_widget = DictionaryOptionsPanel(self)

        self.initial_selection_widget = DictionaryInitialSelectionsWidget(self)

        self.progress_bar = DictionaryProgressBar(self)
        self.go_back_button = GoBackToFilterChoiceButton(self)

    def _setup_labels(self):
        self.currently_displaying_label = CurrentlyDisplayingIndicatorLabel(self)
        self.sequence_count_label = SequenceCountLabel(self)

    def resize_dictionary_browser(self):
        """Resize all necessary widgets in the dictionary browser."""
        self.scroll_widget.resize_dictionary_browser_scroll_widget()
        self.go_back_button.resize_go_back_button()
        self.currently_displaying_label.resize_currently_displaying_label()
        self.sequence_count_label.resize_sequence_count_label()
        self.initial_selection_widget.resize_initial_selections_widget()
        self.nav_sidebar.resize_nav_sidebar()
