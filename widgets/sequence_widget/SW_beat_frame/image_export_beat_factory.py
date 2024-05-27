import os
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtGui import QImage

from path_helpers import get_my_photos_path
from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.sequence_image_export_manager import (
        SequenceImageExportManager,
    )


class ImageExportBeatFactory:
    def __init__(self, export_manager: "SequenceImageExportManager"):
        self.export_manager = export_manager
        self.beat_frame = export_manager.beat_frame
        self.sequence_widget = export_manager.sequence_widget

    def process_sequence_to_beats(self, sequence: list[dict])-> list[BeatView]:
        from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame

        self.temp_beat_frame = SW_BeatFrame(self.sequence_widget)
        filled_beats = []
        for i, beat_data in enumerate(sequence[2:], start=2):
            beat_view = self.create_beat_view_from_data(beat_data, i - 1)
            filled_beats.append(beat_view)
        return filled_beats

    def create_beat_view_from_data(self, beat_data, number):
        new_beat_view = BeatView(self.temp_beat_frame)
        beat = Beat(self.temp_beat_frame)
        beat.pictograph_dict = beat_data
        beat.updater.update_pictograph(beat_data)
        new_beat_view.set_beat(beat, number)
        return new_beat_view
