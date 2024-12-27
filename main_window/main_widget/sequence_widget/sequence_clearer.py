from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class SequenceClearer:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_manager = sequence_widget.main_widget.json_manager
        self.manual_builder = None
        self.settings_manager = sequence_widget.main_widget.settings_manager

    def clear_sequence(
        self, show_indicator=True, should_reset_to_start_pos_picker=True
    ) -> None:
        if not self.manual_builder:
            self.manual_builder = self.sequence_widget.main_widget.construct_tab
        # if the user is on the advanced start pos picker tab, then don't reset to the start pos picker

        self.json_manager.loader_saver.clear_current_sequence_file()
        self._reset_beat_frame()
        self._initialize_manual_builder()
        self._reset_manual_builder(should_reset_to_start_pos_picker)
        self._show_clear_indicator(show_indicator)
        self.sequence_widget.graph_editor.state.reset_graph_editor()
        self._configure_beat_frame()
        self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _initialize_manual_builder(self) -> None:
        if not self.manual_builder:
            self.manual_builder = self.sequence_widget.main_widget.construct_tab

    def _reset_manual_builder(self, should_reset_to_start_pos_picker: bool) -> None:
        if should_reset_to_start_pos_picker:
            self.manual_builder.reset_to_start_pos_picker()
        self.manual_builder.last_beat = self.sequence_widget.beat_frame.start_pos
        self.graph_editor = self.sequence_widget.graph_editor
        # self.graph_editor.adjustment_panel.blue_ori_picker.set_initial_orientation(IN)
        # self.graph_editor.adjustment_panel.red_ori_picker.set_initial_orientation(IN)

    def _show_clear_indicator(self, show_indicator: bool) -> None:
        if show_indicator:
            self.sequence_widget.indicator_label.show_message("Sequence cleared")

    def _configure_beat_frame(self) -> None:
        if self.settings_manager.global_settings.get_grow_sequence():
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(0)

    def _reset_beat_frame(self) -> None:
        self.beat_frame = self.sequence_widget.beat_frame
        for beat_view in self.beat_frame.beats:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False
        self.sequence_widget.beat_frame.start_pos_view.setScene(
            self.beat_frame.start_pos_view.blank_beat
        )
        self.beat_frame.start_pos_view.is_filled = False
        self.beat_frame.selection_overlay.deselect_beat()
        self.beat_frame.sequence_widget.current_word_label.update_current_word_label_from_beats()
