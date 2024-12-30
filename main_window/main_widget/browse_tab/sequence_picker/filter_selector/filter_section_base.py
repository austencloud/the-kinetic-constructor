from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt

from ..sequence_picker_go_back_button import SequencePickerGoBackButton

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.filter_selector.sequence_picker_filter_selector import SequencePickerFilterSelector


class FilterSectionBase(QWidget):
    def __init__(
        self, filter_selector: "SequencePickerFilterSelector", label_text: str
    ):
        super().__init__(filter_selector)
        self.filter_selector = filter_selector
        self.buttons: dict[str, QPushButton] = {}
        self.sequence_picker = filter_selector.sequence_picker
        self.browse_tab = filter_selector.browse_tab
        self.main_widget = filter_selector.browse_tab.main_widget
        self.metadata_extractor = self.main_widget.metadata_extractor
        self._setup_ui(label_text)

        self.initialized = False

    def _setup_ui(self, label_text: str):
        layout = QVBoxLayout(self)

        top_bar_layout = QHBoxLayout()
        self.go_back_button = SequencePickerGoBackButton(
            self.filter_selector.sequence_picker
        )
        self.go_back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.go_back_button.connect_button(
            self.filter_selector.show_filter_choice_widget
        )
        top_bar_layout.addWidget(
            self.go_back_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        top_bar_layout.addStretch(1)

        layout.addLayout(top_bar_layout)

        self.header_label = QLabel(label_text)
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.header_label)
        layout.addStretch(1)
        self.setLayout(layout)

        self.go_back_button.hide()
        self.header_label.hide()
