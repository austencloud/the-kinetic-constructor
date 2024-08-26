from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt


from widgets.sequence_builder.components.start_pos_picker.choose_your_next_pictograph_label import (
    ChooseYourNextPictographLabel,
)
from widgets.sequence_builder.option_picker.option_manager import OptionManager

from .scroll_area.option_picker_scroll_area import OptionPickerScrollArea

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class OptionPicker(QWidget):
    """Contains the "Choose Your Next Pictograph" label and the OptionPickerScrollArea."""

    option_selected = pyqtSignal(str)

    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.json_manager = self.main_widget.json_manager
        self.choose_your_next_pictograph_label = ChooseYourNextPictographLabel(self)
        self.option_manager = OptionManager(self)
        self.scroll_area = OptionPickerScrollArea(self)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 200);")
        self.setup_layout()
        self.disabled = False
        self.hide()

    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_your_next_pictograph_label.show()

        header_label_layout = QHBoxLayout()
        header_label_layout.addStretch(1)
        header_label_layout.addWidget(self.choose_your_next_pictograph_label)
        header_label_layout.addStretch(1)
        self.layout.addLayout(header_label_layout, 1)
        self.layout.addWidget(self.scroll_area, 14)

    def update_option_picker(self):
        if self.disabled:
            return
        sequence = self.json_manager.loader_saver.load_current_sequence_json()

        if len(sequence) > 1:
            next_options: dict = self.option_manager.get_next_options(sequence)
            self.scroll_area._hide_all_pictographs()
            self.scroll_area.add_and_display_relevant_pictographs(next_options)
        self.choose_your_next_pictograph_label.set_stylesheet()

    def resize_option_picker(self) -> None:
        self.choose_your_next_pictograph_label.resize_choose_your_next_option_label()
        self.scroll_area.resize_option_picker_scroll_area()

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        self.scroll_area.set_disabled(disabled)
