from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .beat import BeatView
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatDurationManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame


class BeatDurationManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame


class BeatDurationManager:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame

    def update_beat_duration(self, changed_beat_view: "BeatView", new_duration: int):
        """
        Update the beat duration, change the beat number to reflect the new duration,
        and update subsequent beats' numbering.
        """
        index = self.beat_frame.beats.index(changed_beat_view)
        current_beat = changed_beat_view.beat

        # Update the duration of the current beat
        current_beat.duration = new_duration

        # Update the beat number display to show the range (e.g., "1-2")
        changed_beat_view.add_beat_number(index + 1)

        # Adjust subsequent beats' numbers after increasing duration
        self.update_beat_numbers()

        # Update the sequence in JSON
        self.beat_frame.json_manager.updater.update_current_sequence_file_with_beat(
            changed_beat_view
        )

    def update_beat_numbers(self):
        """
        Update the beat numbers for all beats based on their positions and durations.
        """
        current_beat_number = 1
        for beat_view in self.beat_frame.beats:
            beat_view.remove_beat_number()  # Remove old number

            if beat_view.beat:
                beat_view.add_beat_number(current_beat_number)
                current_beat_number += beat_view.beat.duration
            else:
                beat_view.add_beat_number(current_beat_number)
                current_beat_number += 1
