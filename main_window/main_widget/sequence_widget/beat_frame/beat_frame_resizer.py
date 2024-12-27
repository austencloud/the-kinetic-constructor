from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget  # Import QWidget

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatFrameResizer(QWidget):
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        super().__init__(beat_frame)
        self.beat_frame = beat_frame
        self.sequence_widget = beat_frame.sequence_widget

        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.SizeHorCursor)

    def resize_beat_frame(self) -> None:

        width, height = self.calculate_dimensions()
        beat_size = self.calculate_beat_size(width, height)
        self.resize_beats(beat_size)
        self.update_views(beat_size)

    def calculate_dimensions(self) -> tuple[int, int]:
        scrollbar_width = self.sequence_widget.scroll_area.verticalScrollBar().width()

        # Calculate available width for the beat frame
        available_width = (
            self.sequence_widget.main_widget.width() // 2
            - self.sequence_widget.button_panel.width()
            - scrollbar_width
        )

        # Set width to the calculated available width
        width = int(available_width * 0.8)

        # Calculate available height for the beat frame
        available_height = (
            self.sequence_widget.height()
            - self.sequence_widget.graph_editor.height() * 0.8
        )

        return width, available_height

    def calculate_beat_size(self, width: int, height: int) -> int:
        num_cols = max(1, self.beat_frame.layout.columnCount() - 1)
        if num_cols == 0:
            return 0
        return min(int(width // 5), int(height // 6))

    def resize_beats(self, beat_size: int) -> None:
        for beat in self.beat_frame.beats:
            beat.setFixedSize(beat_size, beat_size)
        self.beat_frame.start_pos_view.setFixedSize(beat_size, beat_size)

    def update_views(self, beat_size: int) -> None:
        for beat in self.beat_frame.beats:
            beat.resize_beat_view()
        self.beat_frame.start_pos_view.resize_beat_view()
        self.beat_frame.selection_overlay.update_overlay_position()
