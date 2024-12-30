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
        self.browse_tab: "BrowseTab" = self.sequence_picker.browse_tab
        self.main_widget = self.sequence_picker.main_widget
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.connect_button(lambda: self.switch_to_initial_filter_selection())

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

    def switch_to_initial_filter_selection(self):
        """Switch to the initial selection page in the stacked layout."""
        sequence_viewer = self.browse_tab.sequence_viewer
        sequence_viewer.word_label.setText("")
        self.main_widget.fade_manager.fade_to_tab(
            self.main_widget.left_stack,
            self.main_widget.left_filter_selector_index,
        )

        self.browse_tab.sequence_viewer.clear()
        self.browse_tab.browse_tab_settings.set_current_section("filter_choice")
        self.browse_tab.browse_tab_settings.set_current_filter(None)
        self.sequence_picker.filter_selector.show_section("filter_choice")
