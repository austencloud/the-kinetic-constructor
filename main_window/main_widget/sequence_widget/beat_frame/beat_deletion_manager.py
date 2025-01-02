from typing import TYPE_CHECKING

from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)
from main_window.main_widget.sequence_widget.sequence_clearer import SequenceClearer


if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatDeletionManager:
    message = "You can't delete a beat if you haven't selected one."

    def __init__(self, beat_frame: "SequenceWidgetBeatFrame") -> None:
        self.beat_frame = beat_frame
        self.construct_tab = None
        self.selection_overlay = self.beat_frame.selection_overlay
        self.json_manager = self.beat_frame.json_manager
        self.settings_manager = self.beat_frame.settings_manager

    def delete_selected_beat(self) -> None:
        selected_beat = self.selection_overlay.get_selected_beat()
        if not selected_beat:
            self._show_no_beat_selected_message()
            return

        if isinstance(selected_beat, StartPositionBeatView):
            self._delete_start_position()
        else:
            self._delete_regular_beat(selected_beat)

    def _show_no_beat_selected_message(self) -> None:
        self.beat_frame.main_widget.sequence_widget.indicator_label.show_message(
            self.message
        )

    def _delete_start_position(self) -> None:
        sequence_clearer = SequenceClearer(self.beat_frame.sequence_widget)
        sequence_clearer.clear_sequence(show_indicator=True)

    def _delete_regular_beat(self, selected_beat: BeatView) -> None:
        beats = self.beat_frame.beats
        widgets = [
            self.beat_frame.start_pos_view,
            self.selection_overlay,
            self.beat_frame.sequence_widget.current_word_label,
            self.beat_frame.sequence_widget.difficulty_label,
        ] + beats
        widgets_to_fade = [selected_beat] + widgets

        self.beat_frame.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets_to_fade,
            callback=lambda: self._finalize_regular_beat_deletion(selected_beat),
            duration=300,
        )

    def _finalize_regular_beat_deletion(self, selected_beat: BeatView) -> None:
        beats = self.beat_frame.beats
        if selected_beat == beats[0]:
            self._delete_first_beat(selected_beat)
        else:
            self._delete_non_first_beat(selected_beat)
        self._post_deletion_updates()

    def _delete_first_beat(self, selected_beat: BeatView) -> None:
        self.selection_overlay.select_beat(
            self.beat_frame.start_pos_view, toggle_graph_editor=False
        )
        self.beat_frame.main_widget.construct_tab.last_beat = (
            self.beat_frame.start_pos_view.beat
        )
        self._delete_beat_and_following(selected_beat)

    def _delete_non_first_beat(self, selected_beat: BeatView) -> None:
        self._delete_beat_and_following(selected_beat)
        last_filled_beat = self.beat_frame.get.last_filled_beat()
        self.selection_overlay.select_beat(last_filled_beat, toggle_graph_editor=False)
        self.beat_frame.main_widget.construct_tab.last_beat = last_filled_beat.beat

    def _delete_beat_and_following(self, start_beat: BeatView) -> None:
        beats = self.beat_frame.beats
        start_index = beats.index(start_beat)
        for beat in beats[start_index:]:
            self._delete_beat(beat)

    def _delete_beat(self, beat: BeatView) -> None:
        beat.setScene(beat.blank_beat)
        beat.is_filled = False

    def _post_deletion_updates(self) -> None:
        self.json_manager.updater.clear_and_repopulate_json_from_beat_view()
        if self.settings_manager.global_settings.get_grow_sequence():
            self.beat_frame.layout_manager.adjust_layout_to_sequence_length()
        self.beat_frame.sequence_widget.current_word_label.update_current_word_label_from_beats()
        self.beat_frame.main_widget.construct_tab.option_picker.update_option_picker()
