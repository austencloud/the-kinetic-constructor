from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import pyqtSignal
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
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.sequence_builder = sequence_builder
        self.main_widget = sequence_builder.main_widget
        self.scroll_area = OptionPickerScrollArea(self)
        self.letter_button_frame = OptionPickerLetterButtonFrame(sequence_builder)
        self.pictograph_factory = ScrollAreaPictographFactory(self.scroll_area)
        self.placeholder = QLabel("Select a start position first.")
        self.layout.addWidget(self.placeholder)
        self.hide()
        self._setup_layout()

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.left_layout.addWidget(self.scroll_area)
        self.right_layout.addWidget(self.letter_button_frame)

        self.layout.addLayout(self.left_layout, 5)
        self.layout.addLayout(self.right_layout, 1)
        self.letter_button_frame.hide()

    def update_options(self, options):
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not options:
            self.layout.addWidget(QLabel("No options available."))
            return

        for option in options:
            optionLabel = QLabel(option)
            self.layout.addWidget(optionLabel)
