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
            lambda: self._on_sequence_length_changed(self.value())
        )

    def _on_sequence_length_changed(self, new_length: int):
        self.controls_widget = self.length_selector.controls_widget
        self.layout_dropdown = self.controls_widget.layout_selector.layout_dropdown
        self.num_beats = new_length
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.current_layout = (
            self.length_selector.layout_tab.layout_settings.get_layout_setting(
                str(self.num_beats)
            )
        )
        self.layout_dropdown.clear()
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        layout_text = f"{self.current_layout[0]} x {self.current_layout[1]}"
        self.layout_dropdown.setCurrentText(layout_text)

        self.controls_widget.beat_frame.update_preview()
        self.controls_widget.default_layout_label.setText(f"Default: {layout_text}")

