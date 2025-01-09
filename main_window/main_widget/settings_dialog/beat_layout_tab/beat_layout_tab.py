from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from .layout_controls import LayoutControls
from .layout_beat_frame import LayoutBeatFrame
from data.beat_frame_layout_options import beat_frame_layout_options

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class BeatLayoutTab(QWidget):
    num_beats: int = 16

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.main_widget = settings_dialog.main_widget
        self.sequence_widget = self.main_widget.sequence_widget
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.current_layout = self.valid_layouts[0]
        self.layout_settings = self.main_widget.settings_manager.sequence_layout
        self.beat_frame = LayoutBeatFrame(self)
        self.controls = LayoutControls(self)

        # Connect signals
        self.controls.sequence_length_spinbox_changed.connect(self._on_sequence_length_changed)
        self.controls.layout_selected.connect(self._on_layout_selected)
        self.controls.update_default_layout.connect(self._set_default_layout)

        self._setup_layout()

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.controls)
        layout.addWidget(self.beat_frame, stretch=1)
        self.setLayout(layout)

    def _on_sequence_length_changed(self, new_length: int):
        self.num_beats = new_length
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.current_layout = self.valid_layouts[0]
        self.controls.layout_dropdown.clear()
        self.controls.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        self.beat_frame.update_preview()
        self._set_default_layout()
        
    def _on_layout_selected(self, layout_text: str):
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.current_layout = (rows, cols)
            self.beat_frame.update_preview()

    def _set_default_layout(self):
        self.layout_settings.set_layout_setting(str(self.num_beats), list(self.current_layout))
        self.controls.default_layout_label.setText(
            f"Default: {self.current_layout[0]} x {self.current_layout[1]}"
        )
