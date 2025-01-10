from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtCore import Qt
from data.beat_frame_layout_options import beat_frame_layout_options

if TYPE_CHECKING:
    from .layout_selector import LayoutSelector


class LayoutDropdown(QComboBox):
    def __init__(self, layout_selector: "LayoutSelector"):
        super().__init__(layout_selector)
        self.layout_selector = layout_selector
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._populate_dropdown()

    def _populate_dropdown(self):
        num_beats = self.layout_selector.controls_widget.layout_tab.num_beats
        self.valid_layouts = beat_frame_layout_options.get(num_beats, [(1, 1)])
        valid_layout_strs = [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        self.addItems(valid_layout_strs)
        self.currentTextChanged.connect(
            lambda layout: self.layout_selector.controls_widget.layout_selected.emit(
                layout
            )
        )
        
