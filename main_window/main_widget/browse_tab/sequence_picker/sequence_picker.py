from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy

from main_window.main_widget.browse_tab.sequence_picker.sequence_picker_filter_selector.sequence_picker_filter_selector import (
    SequencePickerFilterSelector,
)
from main_window.main_widget.browse_tab.sequence_picker.sequence_picker_go_back_button import (
    SequencePickerGoBackButton,
)

from .sequence_picker_nav_sidebar import SequencePickerNavSidebar
from .sequence_picker_scroll_widget import SequencePickerScrollWidget
from .currently_displaying_label import (
    CurrentlyDisplayingLabel,
)
from .sequence_picker_progress_bar import SequencePickerPirogressBar
from .sequence_picker_count_label import SequencePickerCountLabel
from .sequence_picker_sort_widget import SequencePickerSortWidget

if TYPE_CHECKING:
    from ..browse_tab import BrowseTab


class SequencePicker(QWidget):
    def __init__(self, browse_tab: "BrowseTab"):
        super().__init__(browse_tab)
        self.browse_tab = browse_tab
        self.main_widget = browse_tab.main_widget
        self._setup_ui()

    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(5)

        self.go_back_button = SequencePickerGoBackButton(self)
        self.currently_displaying_label = CurrentlyDisplayingLabel(self)
        self.count_label = SequencePickerCountLabel(self)
        self.progress_bar = SequencePickerPirogressBar(self)
        self.sort_widget = SequencePickerSortWidget(self)
        self.scroll_widget = SequencePickerScrollWidget(self)
        self.nav_sidebar = SequencePickerNavSidebar(self)
        self.filter_selector = SequencePickerFilterSelector(self)

        self.main_layout.addWidget(self.go_back_button)
        self.main_layout.addWidget(self.currently_displaying_label)
        self.main_layout.addWidget(self.count_label)
        self.main_layout.addWidget(self.sort_widget)
        self.main_layout.addWidget(self.progress_bar)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.nav_sidebar, 1)
        content_layout.addWidget(self.scroll_widget, 9)

        self.main_layout.addLayout(content_layout)

        self.setLayout(self.main_layout)
