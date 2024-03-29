from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt

from widgets.sequence_builder.components.option_picker.option_manager import (
    OptionManager,
)
from widgets.sequence_builder.components.start_pos_picker.choose_your_next_option_label import (
    ChooseYourNextOptionLabel,
)

from .option_picker_scroll_area import OptionPickerScrollArea

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder


class OptionPicker(QWidget):
    option_selected = pyqtSignal(str)  # Signal to emit the selected option

    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.option_manager = OptionManager(self)
        self.scroll_area = OptionPickerScrollArea(self)
        self.choose_your_next_option_label = ChooseYourNextOptionLabel(self)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setup_layout()
        self.hide()

    def setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.choose_your_next_option_label.show()
        self.layout.addWidget(self.choose_your_next_option_label, 1)
        self.layout.addWidget(self.scroll_area, 10)

    def update_option_picker(self):
        current_sequence_json_handler = (
            self.main_widget.json_manager.current_sequence_json_handler
        )
        sequence = current_sequence_json_handler.load_current_sequence_json()

        if sequence:
            next_options: dict = self.option_manager.get_next_options(sequence)
            self.scroll_area._hide_all_pictographs()
            self.scroll_area.add_and_display_relevant_pictographs(next_options)
        self.choose_your_next_option_label.set_stylesheet()
