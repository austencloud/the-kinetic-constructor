from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QGridLayout
from data.beat_frame_layouts import SEQUENCE_WIDGET_BEAT_FRAME_LAYOUTS
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWorkbenchBeatFrame


class SequenceWorkbenchBeatFrameLayoutManager:
    def __init__(self, beat_frame: "SequenceWorkbenchBeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_overlay
        self.settings_manager = beat_frame.main_widget.main_window.settings_manager

    def setup_layout(self) -> None:
        layout: QGridLayout = QGridLayout(self.beat_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.beat_frame.start_pos_view.start_pos.initializer.set_nonradial_points_visibility(
            False
        )
        layout.addWidget(self.beat_frame.start_pos_view, 0, 0)
        for i, beat in enumerate(self.beat_frame.beat_views):
            row, col = divmod(i, 8)
            layout.addWidget(beat, row + 1, col + 1)
        self.beat_frame.layout = layout
        self.configure_beat_frame(16)

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return SEQUENCE_WIDGET_BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))

    def get_cols(self):
        layout = self.beat_frame.layout
        cols = 0
        for i in range(layout.columnCount()):
            if layout.itemAtPosition(0, i):
                cols += 1
        return cols - 1

    def get_rows(self):
        layout = self.beat_frame.layout
        rows = 0
        for i in range(layout.rowCount()):
            if layout.itemAtPosition(i, 1):
                rows += 1
        return rows

    def configure_beat_frame_for_filled_beats(self) -> None:
        if self.settings_manager.global_settings.get_grow_sequence():
            filled_beats = [
                beat for beat in self.beat_frame.beat_views if beat.is_filled
            ]
            self.beat_frame.layout_manager.configure_beat_frame(len(filled_beats))

    def configure_beat_frame(self, num_beats, override_grow_sequence=False):
        if not override_grow_sequence:
            grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
            if grow_sequence:
                num_filled_beats = self.beat_frame.get.next_available_beat() or 0
                num_beats = num_filled_beats
        columns, rows = self.calculate_layout(num_beats)

        self.beat_frame.sequence_widget.scroll_area.verticalScrollBarPolicy = (
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            if rows > 4
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.rearrange_beats(num_beats, columns, rows)

    def rearrange_beats(self, num_beats, columns, rows):
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beat_views
        for row in range(rows):
            for col in range(1, columns + 1):
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
        selected_beat = self.selection_manager.selected_beat
        if selected_beat:
            # self.selection_manager.deselect_beat()
            # self.selection_manager.select_beat(selected_beat, toggle_graph_editor=False)
            self.selection_manager.update_overlay_position()

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.beat_frame.get.next_available_beat()
        self.configure_beat_frame(last_filled_index)

    def calculate_current_layout(self) -> tuple:
        layout = self.beat_frame.layout

        max_row = 0
        max_col = 0

        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and isinstance(item.widget(), BeatView):
                position = layout.getItemPosition(i)
                max_row = max(max_row, position[0])
                max_col = max(max_col, position[1])

        return max_row + 1, max_col  # Add 1 to max_row to get the count
