from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from data.beat_frame_layouts import BEAT_FRAME_LAYOUTS

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame


class SW_BeatFrameLayoutManager:
    def __init__(self, beat_frame: "SW_BeatFrame"):
        self.beat_frame = beat_frame
        self.selection_manager = beat_frame.selection_manager
        self.settings_manager = beat_frame.main_widget.main_window.settings_manager

    def calculate_layout(self, beat_count: int) -> tuple[int, int]:
        return BEAT_FRAME_LAYOUTS.get(beat_count, (1, beat_count))

    def configure_beat_frame(self, num_beats):
        grow_sequence = self.settings_manager.get_grow_sequence()
        if grow_sequence:
            num_filled_beats = self.beat_frame.find_next_available_beat() or 0
            num_beats = num_filled_beats
        columns, rows = self.calculate_layout(num_beats)

        self.beat_frame.sequence_widget.scroll_area.verticalScrollBarPolicy = (
            Qt.ScrollBarPolicy.ScrollBarAlwaysOn
            if rows > 4
            else Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        # QApplication.processEvents()
        self.rearrange_beats(num_beats, columns, rows)


    def rearrange_beats(self, num_beats, columns, rows):
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beats
        for row in range(rows):
            for col in range(1, columns + 1):
                if index < num_beats:
                    beat_view = beats[index]
                    self.beat_frame.layout.addWidget(beat_view, row, col)
                    beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1

        self.beat_frame.adjustSize()
        selected_beat = self.selection_manager.selected_beat
        if selected_beat:
            self.selection_manager.deselect_beat()
            self.selection_manager.select_beat(selected_beat)
            self.selection_manager.update_overlay_position()