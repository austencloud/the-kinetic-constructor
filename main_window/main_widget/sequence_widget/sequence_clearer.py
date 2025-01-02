from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class SequenceClearer:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.json_manager = sequence_widget.main_widget.json_manager
        self.construct_tab = None
        self.settings_manager = sequence_widget.main_widget.settings_manager
        self.main_widget = sequence_widget.main_widget

    def clear_sequence(self, show_indicator=True) -> None:
        beat_frame = self.sequence_widget.beat_frame
        if not self.construct_tab:
            self.construct_tab = self.sequence_widget.main_widget.construct_tab
        beats = beat_frame.beats
        widgets = [
            self.sequence_widget.current_word_label,
            self.sequence_widget.difficulty_label,
            beat_frame.start_pos_view,
            beat_frame.selection_overlay,
        ] + beats
        beats_filled = any(beat.is_filled for beat in beats)
        start_pos_filled = beat_frame.start_pos_view.is_filled

        if not beats_filled and not start_pos_filled:
            self.main_widget.fade_manager.widget_fader.fade_and_update(
                widgets,
                callback=lambda: self.reset_widgets(show_indicator),
                duration=300,
            )
        elif (
            self.main_widget.right_stack.currentWidget()
            == self.main_widget.generate_tab
        ):
            self.main_widget.fade_manager.widget_fader.fade_and_update(
                widgets,
                callback=lambda: self.reset_widgets(show_indicator),
                duration=300,
            )
        else:
            self.main_widget.fade_manager.widget_and_stack_fader.fade_widgets_and_stack(
                widgets,
                self.main_widget.right_stack,
                self.main_widget.right_start_pos_picker_index,
                300,
                lambda: self.reset_widgets(show_indicator),
            )

    def reset_widgets(self, show_indicator):
        self.json_manager.loader_saver.clear_current_sequence_file()
        self._reset_beat_frame()
        self._show_clear_indicator(show_indicator)
        self._configure_beat_frame()
        self.sequence_widget.graph_editor.state.reset_graph_editor()
        self.construct_tab.last_beat = self.sequence_widget.beat_frame.start_pos
        self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _reset_construct_tab(self) -> None:
        current_widget = self.main_widget.right_stack.currentWidget()
        if not current_widget == self.main_widget.generate_tab:
            self.construct_tab.transition_to_start_pos_picker()
        self.graph_editor = self.sequence_widget.graph_editor

    def _show_clear_indicator(self, show_indicator: bool) -> None:
        if show_indicator:
            self.sequence_widget.indicator_label.show_message("Sequence cleared")

    def _configure_beat_frame(self) -> None:
        if self.settings_manager.global_settings.get_grow_sequence():
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(0)

    def _reset_beat_frame(self) -> None:
        beat_frame = self.sequence_widget.beat_frame
        for beat_view in beat_frame.beats:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False
        self.sequence_widget.beat_frame.start_pos_view.setScene(
            beat_frame.start_pos_view.blank_beat
        )
        beat_frame.start_pos_view.is_filled = False
        beat_frame.selection_overlay.deselect_beat()
        beat_frame.sequence_widget.current_word_label.update_current_word_label_from_beats()
