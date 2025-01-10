from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from main_window.main_widget.settings_dialog.beat_layout_tab.layout_length_button import (
    LayoutLengthButton,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.num_beats_spinbox import (
    NumBeatsSpinbox,
)
from main_window.main_widget.settings_dialog.beat_layout_tab.sequence_length_label import (
    SequenceLengthLabel,
)

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget


class LengthSelector(QFrame):
    def __init__(self, controls_widget: "LayoutControlsWidget"):
        super().__init__(controls_widget)
        self.controls_widget = controls_widget
        self.layout_tab = controls_widget.layout_tab
        self.sequence_length_label = SequenceLengthLabel(self)
        self.minus_button = LayoutLengthButton("-", self, self._decrease_length)
        self.plus_button = LayoutLengthButton("+", self, self._increase_length)
        self.num_beats_spinbox = NumBeatsSpinbox(self)

        self._setup_layout()

    def _setup_layout(self):
        spinbox_layout = QHBoxLayout()
        spinbox_layout.setSpacing(10)
        spinbox_layout.addWidget(self.minus_button)
        spinbox_layout.addWidget(self.num_beats_spinbox)
        spinbox_layout.addWidget(self.plus_button)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.sequence_length_label)
        main_layout.addLayout(spinbox_layout)

    def _decrease_length(self):
        """Decrease the sequence length and emit the change."""
        current_value = self.num_beats_spinbox.value()
        if current_value > 1:
            self.num_beats_spinbox.setValue(current_value - 1)

    def _increase_length(self):
        """Increase the sequence length and emit the change."""
        self.num_beats_spinbox.setValue(self.num_beats_spinbox.value() + 1)
