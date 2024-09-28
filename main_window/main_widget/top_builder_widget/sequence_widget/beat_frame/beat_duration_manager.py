from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beat import BeatView
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatDurationManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        self.json_duration_updater = beat_frame.json_manager.updater.duration_updater

    def update_beat_duration(
        self, changed_beat_view: "BeatView", new_duration: int
    ) -> None:
        """
        Update the beat duration, adjust beat numbering, and update the JSON file.
        """
        index = self.beat_frame.beats.index(changed_beat_view)
        current_beat = changed_beat_view.beat

        # Update the beat duration in the view
        current_beat.duration = new_duration
        changed_beat_view.add_beat_number()

        # Adjust subsequent beats' numbers after duration change
        self.update_beat_numbers()

        # Delegate JSON update to JsonDurationUpdater
        self.json_duration_updater.update_beat_duration_in_json(
            changed_beat_view, new_duration
        )

    def update_beat_numbers(self) -> None:
        """
        Update beat numbers for all beats based on their positions and durations.
        """
        current_beat_number = 1
        for beat_view in self.beat_frame.beats:
            beat_view.remove_beat_number()  # Remove the old number

            if beat_view.beat:
                beat_view.beat.beat_number = current_beat_number
                beat_view.add_beat_number()
                current_beat_number += beat_view.beat.duration
            else:
                beat_view.blank_beat.beat_number = current_beat_number
                beat_view.add_beat_number()
                current_beat_number += 1
