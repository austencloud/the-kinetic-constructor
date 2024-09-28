from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.beat_frame.beat import (
        Beat,
    )
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatAdder:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        self.beats = beat_frame.beats
        self.sequence_widget = beat_frame.sequence_widget
        self.main_widget = beat_frame.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.json_manager = self.main_widget.json_manager

    def add_beat_to_sequence(
        self, new_beat: "Beat", override_grow_sequence=False, update_word=True
    ) -> None:
        next_beat_index = self.beat_frame.get.next_available_beat()
        if next_beat_index == 0:
            self.sequence_widget.difficulty_label.set_difficulty_level(1)
        grow_sequence = self.settings_manager.global_settings.get_grow_sequence()
        if grow_sequence and not override_grow_sequence:
            if (
                next_beat_index is not None
                and self.beats[next_beat_index].is_filled is False
            ):
                self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
                self.json_manager.updater.update_current_sequence_file_with_beat(
                    self.beats[next_beat_index]
                )
                if update_word:
                    self.sequence_widget.update_current_word()
                self.beat_frame.layout_manager.adjust_layout_to_sequence_length()
                self.sequence_builder = (
                    self.main_widget.top_builder_widget.sequence_builder
                )
                self.sequence_builder.manual_builder.last_beat = self.beats[
                    next_beat_index
                ].beat

        elif not grow_sequence or override_grow_sequence:
            if (
                next_beat_index is not None
                and self.beats[next_beat_index].is_filled is False
                and self.beats[next_beat_index].isVisible()
            ):
                self.beats[next_beat_index].set_beat(new_beat, next_beat_index + 1)
                self.json_manager.updater.update_current_sequence_file_with_beat(
                    self.beats[next_beat_index]
                )
                if update_word:
                    self.sequence_widget.update_current_word()
                self.sequence_builder = (
                    self.main_widget.top_builder_widget.sequence_builder
                )
                self.sequence_builder.manual_builder.last_beat = self.beats[
                    next_beat_index
                ].beat
