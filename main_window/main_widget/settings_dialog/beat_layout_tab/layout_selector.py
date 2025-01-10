import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from .layout_dropdown import LayoutDropdown
from .select_layout_label import SelectLayoutLabel

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget
    
BEAT_FRAME_LAYOUT_OPTIONS_PATH = "data/beat_frame_layout_options.json"


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
        beat_frame_layout_options = self.load_beat_frame_layout_options(
            BEAT_FRAME_LAYOUT_OPTIONS_PATH
        )
        self.valid_layouts = beat_frame_layout_options.get(num_beats, [(1, 1)])

    def load_beat_frame_layout_options(
        self, file_path: str
    ) -> dict[int, list[list[int]]]:
        try:
            with open(file_path, "r") as f:
                return {int(key): value for key, value in json.load(f).items()}
        except FileNotFoundError:
            print(f"File not found: {file_path}. Using default options.")
            return {}

    def _setup_layout(self):
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.layout_dropdown_label)
        self.layout.addWidget(self.layout_dropdown)

    def resizeEvent(self, event):
        self.layout.setSpacing(self.controls_widget.layout_tab.width() // 50)
