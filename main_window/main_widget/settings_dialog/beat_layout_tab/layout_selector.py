from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from data.beat_frame_layout_options import beat_frame_layout_options

from .layout_dropdown import (
    LayoutDropdown,
)
from .select_layout_label import (
    SelectLayoutLabel,
)

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget


class LayoutSelector(QFrame):
    def __init__(self, controls_widget: "LayoutControlsWidget"):
        super().__init__(controls_widget)
        self.controls_widget = controls_widget
        self.layout_tab = controls_widget.layout_tab
        num_beats = self.controls_widget.layout_tab.num_beats
        self._update_valid_layouts(num_beats)

        self.layout_dropdown_label = SelectLayoutLabel(self)
        self.layout_dropdown = LayoutDropdown(self)
        self._setup_layout()

    def _update_valid_layouts(self, num_beats):
        self.valid_layouts =  beat_frame_layout_options.get(num_beats, [(1, 1)])

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.layout_dropdown_label)
        self.layout.addWidget(self.layout_dropdown)

    def resizeEvent(self, event):
        self.layout.setSpacing(self.controls_widget.layout_tab.width() // 50)
