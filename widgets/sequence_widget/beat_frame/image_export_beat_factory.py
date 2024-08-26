from typing import TYPE_CHECKING, Union

from widgets.sequence_widget.beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.sequence_widget.beat_frame.image_export_manager import (
        ImageExportManager,
    )
    from widgets.sequence_widget.beat_frame.beat_frame import SequenceWidgetBeatFrame
    from widgets.dictionary_widget.temp_beat_frame import (
        TempBeatFrame,
    )


class ImageExportBeatFactory:
    def __init__(
        self,
        export_manager: "ImageExportManager",
        beat_frame_class: Union["SequenceWidgetBeatFrame", "TempBeatFrame"],
    ):
        self.export_manager = export_manager
        self.beat_frame_class = beat_frame_class

    def process_sequence_to_beats(self, sequence: list[dict]) -> list[BeatView]:
        if self.beat_frame_class.__name__ == "SequenceWidgetBeatFrame":
            temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.top_builder_widget.sequence_widget
            )
        elif self.beat_frame_class.__name__ == "TempBeatFrame":
            temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.dictionary_widget
            )
        filled_beats = []
        for i, beat_data in enumerate(sequence[2:], start=2):
            beat_view = self.create_beat_view_from_data(
                beat_data, i - 1, temp_beat_frame
            )
            filled_beats.append(beat_view)
        return filled_beats

    def create_beat_view_from_data(self, beat_data, number, temp_beat_frame):
        new_beat_view = BeatView(temp_beat_frame)
        beat = Beat(temp_beat_frame)
        beat.pictograph_dict = beat_data
        beat.updater.update_pictograph(beat_data)
        new_beat_view.set_beat(beat, number)
        return new_beat_view
