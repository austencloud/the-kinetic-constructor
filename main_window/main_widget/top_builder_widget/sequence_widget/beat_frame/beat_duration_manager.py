from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .beat import BeatView
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame

class BeatDurationManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame

    def update_beat_numbers(self, changed_beat_view: "BeatView"):
        index = self.beat_frame.beats.index(changed_beat_view)
        current_beat_number = changed_beat_view.number + changed_beat_view.beat.duration
        changed_beat_view.beat.pictograph_dict["duration"] = (
            changed_beat_view.beat.duration
        )
        self.beat_frame.json_manager.updater.update_current_sequence_file_with_beat(
            changed_beat_view
        )
        for beat_view in self.beat_frame.beats[index + 1 :]:
            beat_view.remove_beat_number()
            beat_view.number = current_beat_number
            beat_view.add_beat_number()
            current_beat_number += beat_view.beat.duration if beat_view.beat else 1
