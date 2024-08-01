from typing import TYPE_CHECKING, Union

from widgets.sequence_widget.SW_beat_frame.beat import Beat, BeatView

if TYPE_CHECKING:
    from widgets.dictionary_widget.invisible_dictionary_beat_frame import (
        InvisibleDictionaryBeatFrame,
    )
    from widgets.sequence_widget.SW_beat_frame.SW_beat_frame import SW_BeatFrame
    from widgets.sequence_widget.SW_beat_frame.image_export_manager import (
        ImageExportManager,
    )


class ImageExportBeatFactory:
    def __init__(
        self,
        export_manager: "ImageExportManager",
        beat_frame_class: Union["SW_BeatFrame", "InvisibleDictionaryBeatFrame"],
    ):
        self.export_manager = export_manager
        self.beat_frame_class = beat_frame_class

    def process_sequence_to_beats(self, sequence: list[dict]) -> list[BeatView]:
        # if the beat frame class is a SW_BeatFrame, then we need to pass the sequence widget
        # if it's a InvisibleDictionaryBeatFrame, then we need to pass the dictionary widget
        if self.beat_frame_class.__name__ == "SW_BeatFrame":
            self.temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.top_builder_widget.sequence_widget
            )
        elif self.beat_frame_class.__name__ == "InvisibleDictionaryBeatFrame":
            self.temp_beat_frame = self.beat_frame_class(
                self.export_manager.main_widget.dictionary_widget
            )
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
