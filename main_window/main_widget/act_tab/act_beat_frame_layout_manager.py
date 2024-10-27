from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QGridLayout
from data.act_beat_frame_layouts import ACT_BEAT_FRAME_LAYOUTS
from data.beat_frame_layouts import SEQUENCE_WIDGET_BEAT_FRAME_LAYOUTS

if TYPE_CHECKING:
    from main_window.main_widget.act_tab.act_beat_frame import ActBeatFrame


class ActBeatFrameLayoutManager:
    def __init__(self, beat_frame: "ActBeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_overlay
        self.settings_manager = beat_frame.main_widget.main_window.settings_manager

    def setup_layout(self) -> None:
        layout: QGridLayout = QGridLayout(self.beat_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.beat_frame.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Start position view can still be added at (0, 0)
        # layout.addWidget(self.beat_frame.start_pos_view, 0, 0)

        # Setup beats (this doesn't take into account the timestamp labels yet)
        for i, beat in enumerate(self.beat_frame.beats):
            row, col = divmod(i, 9)
            layout.addWidget(beat, row + 1, col + 1)  # Adjusted for timestamp column

        self.beat_frame.layout = layout

    def configure_beat_frame(self, num_beats, override_grow_sequence=False):
        columns, rows = self.calculate_layout(num_beats)

        # Ensure vertical scroll when there are too many rows
        self.beat_frame.act_tab.beat_scroll_area.verticalScrollBarPolicy = (
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            if rows > 4
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.rearrange_beats(num_beats, columns, rows)

    def rearrange_beats(self, num_beats, columns, rows):
        # Clear the current layout and hide widgets
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        # Add the start position view at (0, 0)
        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)

        index = 0
        beats = self.beat_frame.beats
        for row in range(rows):

            # Add beats starting from column 1
            for col in range(1, columns + 1):
                if index < num_beats:
                    beat_view = beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row + 1, col)
                    beat_view.remove_beat_number()

                    # Reset numbering for each row from 1 to 8
                    beat_number_in_row = (index % 8) + 1
                    beat_view.add_beat_number(str(beat_number_in_row))

                    beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1

    def adjust_layout_to_sequence_length(self):
        last_filled_index = self.beat_frame.get.next_available_beat()
        self.configure_beat_frame(last_filled_index)

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return ACT_BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))
