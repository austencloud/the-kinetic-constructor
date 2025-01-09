from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from .beat_layout_controls import BeatLayoutControls
from .layout_preview_beat_frame import LayoutPreviewBeatFrame
from data.beat_frame_layouts import beat_frame_layout_options

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class BeatLayoutTab(QWidget):
    """Tab for configuring default beat layouts."""

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.settings_manager = settings_dialog.main_widget.settings_manager
        self.num_beats = 16  # Default to 16 beats
        self.sequence_widget = settings_dialog.main_widget.sequence_widget
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.current_layout = self.valid_layouts[0]
        self.layout_settings = self.settings_manager.sequence_layout
        # Initialize controls and connect signals
        self.controls = BeatLayoutControls(self)
        self.controls.sequence_length_changed.connect(self._on_sequence_length_changed)
        self.controls.layout_selected.connect(self._on_layout_selected)

        # Initialize preview frame
        self.beat_frame = LayoutPreviewBeatFrame(self)

        self._setup_layout()

    def _setup_layout(self):
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.controls)
        self.layout.addWidget(self.beat_frame, stretch=1)

    def _on_sequence_length_changed(self, new_length: int):
        """Handle updates to the sequence length."""
        self.num_beats = new_length
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.controls.layout_dropdown.clear()
        self.controls.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        self.current_layout = self.valid_layouts[0]
        self.controls.num_beats_spinbox.setValue(self.num_beats)
        self.beat_frame.update_preview()
        self.rearrange_beats(self.num_beats)

    def _on_layout_selected(self, layout_text: str):
        """Handle updates to the selected layout."""
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.current_layout = (rows, cols)
            self.beat_frame.update_preview()
            self.rearrange_beats(self.num_beats)
            self.layout_settings.set_layout_setting(
                str(self.num_beats), list(self.current_layout)
            )

    def rearrange_beats(self, num_beats):
        """Update the beat frame to match the selected layout."""
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beat_views
        for row in range(self.beat_frame.rows):
            for col in range(1, self.beat_frame.cols + 1):
                if index < num_beats:
                    if index < len(beats):
                        beat_view = beats[index]
                        self.beat_frame.layout.addWidget(beat_view, row, col)
                        beat_view.beat.beat_number_item.update_beat_number(index + 1)
                        beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1
        self.beat_frame.adjustSize()
