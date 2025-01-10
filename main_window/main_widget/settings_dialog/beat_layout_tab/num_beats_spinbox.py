from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSpinBox
from PyQt6.QtCore import Qt
from data.beat_frame_layout_options import beat_frame_layout_options

if TYPE_CHECKING:
    from .layout_controls_widget import LayoutControlsWidget


class NumBeatsSpinbox(QSpinBox):
    def __init__(self, control_widget: "LayoutControlsWidget"):
        super().__init__(control_widget)
        self.control_widget = control_widget
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setRange(1, 64)
        self.setValue(self.control_widget.layout_tab.num_beats)
        self.valueChanged.connect(
            lambda: self._on_sequence_length_changed(self.value())
        )

    def resizeEvent(self, event):
        font = self.font()
        font.setPointSize(self.control_widget.width() // 50)
        self.setFont(font)

    def _on_sequence_length_changed(self, new_length: int):
        self.num_beats = new_length
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.current_layout = (
            self.control_widget.layout_tab.layout_settings.get_layout_setting(
                str(self.num_beats)
            )
        )
        self.control_widget.layout_selector.layout_dropdown.clear()
        self.control_widget.layout_selector.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        layout_text = f"{self.current_layout[0]} x {self.current_layout[1]}"
        self.control_widget.layout_selector.layout_dropdown.setCurrentText(layout_text)

        self.control_widget.beat_frame.update_preview()
        self.control_widget.default_layout_label.setText(f"Default: {layout_text}")
