from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.sequence_picker.sequence_picker import (
        SequencePicker,
    )
    from main_window.main_widget.browse_tab.browse_tab import BrowseTab


class SequencePickerGoBackButton(QPushButton):
    def __init__(self, sequence_picker: "SequencePicker"):
        super().__init__("Back", cursor=Qt.CursorShape.PointingHandCursor)
        self.sequence_picker = sequence_picker

        # self.hide()
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.connect_button(
            lambda: self.sequence_picker.browse_tab.layout_manager.switch_to_initial_filter_selection()
        )

    def connect_button(self, callback):
        """Connects the button's clicked signal to the provided callback."""
        self.clicked.connect(callback)

    def resizeEvent(self, event):
        """Repositions the button to the top left corner of the widget."""
        self.setFixedHeight(self.sequence_picker.main_widget.height() // 30)
        self.setFixedWidth(self.sequence_picker.main_widget.width() // 30)
        font = self.font()
        font.setPointSize(self.sequence_picker.main_widget.width() // 100)
        self.setFont(font)
        super().resizeEvent(event)
