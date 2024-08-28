from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class SequenceClearer:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_manager = sequence_widget.json_manager
        self.sequence_builder = sequence_widget.top_builder_widget.sequence_builder
        self.beat_frame = sequence_widget.beat_frame
        self.settings_manager = sequence_widget.settings_manager

    def clear_sequence(
        self, show_indicator=True, should_reset_to_start_pos_picker=True
    ) -> None:
        self.json_manager.loader_saver.clear_current_sequence_file()
        self._reset_beat_frame()

        if should_reset_to_start_pos_picker:
            self.sequence_builder.reset_to_start_pos_picker()
        self.sequence_builder.last_beat = self.beat_frame.start_pos
        if show_indicator:
            self.sequence_widget.indicator_label.show_message("Sequence cleared")
        self.sequence_widget.graph_editor.clear_graph_editor()

        if self.settings_manager.global_settings.get_grow_sequence():
            self.beat_frame.layout_manager.configure_beat_frame(0)
        self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _reset_beat_frame(self) -> None:
        for beat_view in self.beat_frame.beats:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False
        self.beat_frame.start_pos_view.setScene(
            self.beat_frame.start_pos_view.blank_beat
        )
        self.beat_frame.start_pos_view.is_filled = False
        self.beat_frame.selection_overlay.deselect_beat()
        self.beat_frame.sequence_widget.update_current_word()
