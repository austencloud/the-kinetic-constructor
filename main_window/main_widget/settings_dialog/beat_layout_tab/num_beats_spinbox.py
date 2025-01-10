from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtCore import Qt
from data.beat_frame_layout_options import beat_frame_layout_options

if TYPE_CHECKING:
    from .length_selector import LengthSelector


class NumBeatsSpinbox(QSpinBox):
    def __init__(self, length_selector: "LengthSelector"):
        super().__init__(length_selector)
        self.length_selector = length_selector
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setRange(1, 64)
        self.setValue(self.length_selector.layout_tab.num_beats)
        self.valueChanged.connect(
            lambda: self.length_selector.on_sequence_length_changed(self.value())
        )
