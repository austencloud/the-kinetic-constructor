from typing import TYPE_CHECKING
from PyQt6.QtCore import QTimer
if TYPE_CHECKING:
    from widgets.sequence_recorder_widget.sequence_recorder_beat_frame import SequenceRecorderBeatFrame


class SequenceRecorderBeatSelectionManager:
    def __init__(self, beat_frame: "SequenceRecorderBeatFrame"):
        self.beat_frame = beat_frame
        self.current_index = 0 
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_selection)

    def set_bpm(self, bpm):
        milliseconds_per_beat = 60000 / bpm
        self.timer.start(milliseconds_per_beat)

    def move_selection(self):
        self.current_index += 1
        if self.current_index >= len(self.beat_frame.beat_views):
            self.current_index = 0 
        self.beat_frame.selection_manager.select_beat(
            self.beat_frame.beat_views[self.current_index]
        )
