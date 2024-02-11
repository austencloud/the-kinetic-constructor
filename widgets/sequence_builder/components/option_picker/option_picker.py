from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

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
        self.scroll_area = OptionPickerScrollArea(self)

        self.setup_layout()
        self.hide()

    def setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.scroll_area)
