from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal

from widgets.pictograph.pictograph import Pictograph
from ....scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)
from .option_picker_scroll_area import OptionPickerScrollArea
from .option_picker_letter_button_frame import OptionPickerLetterButtonFrame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...sequence_builder import SequenceBuilder


class OptionPicker(QWidget):
    option_selected = pyqtSignal(str)  # Signal to emit the selected option

    def __init__(self, sequence_builder: "SequenceBuilder"):
        super().__init__(sequence_builder)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.options: dict[str, Pictograph] = {}
        self.scroll_area = OptionPickerScrollArea(self)

        self.setup_layout()
        self.hide()

    def setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.scroll_area)