from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from main_window.main_widget.browse_tab.sequence_picker.sequence_picker_go_back_button import (
    SequencePickerGoBackButton,
)

from .currently_displaying_label import (
    CurrentlyDisplayingLabel,
)
from .sequence_picker_progress_bar import SequencePickerPirogressBar
from .sequence_picker_count_label import SequencePickerCountLabel
from .sequence_picker_sort_widget import SequencePickerSortWidget

if TYPE_CHECKING:
    pass


class SequencePickerControlPanel(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
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

        self.main_layout.addWidget(self.go_back_button)
        self.main_layout.addWidget(self.currently_displaying_label)
        self.main_layout.addWidget(self.count_label)
        self.main_layout.addWidget(self.sort_widget)
        self.main_layout.addWidget(self.progress_bar)

        self.setLayout(self.main_layout)
