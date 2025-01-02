from typing import TYPE_CHECKING
from main_window.main_widget.sequence_widget.beat_frame.beat_view import BeatView
from main_window.main_widget.sequence_widget.beat_frame.start_pos_beat_view import (
    StartPositionBeatView,
)

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget
    from main_window.main_widget.sequence_widget.beat_frame.sequence_widget_beat_frame import (
        SequenceWidgetBeatFrame,
    )


class BeatRemover:
    message = "You can't delete a beat if you haven't selected one."

    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget
        self.beat_frame = sequence_widget.beat_frame
        self.json_manager = sequence_widget.main_widget.json_manager
        self.settings_manager = sequence_widget.main_widget.settings_manager
        self.main_widget = sequence_widget.main_widget
        self.selection_overlay = self.beat_frame.selection_overlay

    def delete_selected_beat(self) -> None:
        selected_beat = self.selection_overlay.get_selected_beat()
        if not selected_beat:
            self._show_no_beat_selected_message()
            return

        if isinstance(selected_beat, StartPositionBeatView):
            self.clear_sequence(show_indicator=True)
        else:
            self._delete_regular_beat(selected_beat)

    def clear_sequence(self, show_indicator=True) -> None:
        beats = self.beat_frame.beats
        widgets = self._collect_widgets()
        beats_filled = any(beat.is_filled for beat in beats)
        start_pos_filled = self.beat_frame.start_pos_view.is_filled

        if not beats_filled and not start_pos_filled:
            self._fade_and_reset_widgets(widgets, show_indicator)
        elif (
            self.main_widget.right_stack.currentWidget()
            == self.main_widget.generate_tab
        ):
            self._fade_and_reset_widgets(widgets, show_indicator)
        else:
            self.main_widget.fade_manager.widget_and_stack_fader.fade_widgets_and_stack(
                widgets,
                self.main_widget.right_stack,
                self.main_widget.right_start_pos_picker_index,
                300,
                lambda: self.reset_widgets(show_indicator),
            )

    def _fade_and_reset_widgets(self, widgets, show_indicator):
        self.main_widget.fade_manager.widget_fader.fade_and_update(
            widgets,
            callback=lambda: self.reset_widgets(show_indicator),
            duration=300,
        )

    def _delete_regular_beat(self, selected_beat: BeatView) -> None:
        widgets = self._collect_widgets()
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
        self.sequence_widget.main_widget.construct_tab.last_beat = (
            self.beat_frame.start_pos_view.beat
        )
        self._delete_beat_and_following(selected_beat)

    def _delete_non_first_beat(self, selected_beat: BeatView) -> None:
        # self._fade_and_reset_widgets([selected_beat], show_indicator=False)
        self._delete_beat_and_following(selected_beat)
        last_filled_beat = self.beat_frame.get.last_filled_beat()
        self.selection_overlay.select_beat(last_filled_beat, toggle_graph_editor=False)
        self.sequence_widget.main_widget.construct_tab.last_beat = last_filled_beat.beat

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
        self.beat_frame.main_widget.sequence_widget.main_widget.construct_tab.option_picker.update_option_picker()
        self.beat_frame.sequence_widget.difficulty_label.update_difficulty_label()

    def reset_widgets(self, show_indicator):
        self.json_manager.loader_saver.clear_current_sequence_file()
        self._reset_beat_frame()
        self._show_clear_indicator(show_indicator)
        self._configure_beat_frame()
        self.sequence_widget.graph_editor.state.reset_graph_editor()
        self.sequence_widget.main_widget.construct_tab.last_beat = (
            self.sequence_widget.beat_frame.start_pos
        )
        self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _reset_beat_frame(self) -> None:
        beat_frame = self.sequence_widget.beat_frame
        for beat_view in beat_frame.beats:
            beat_view.setScene(beat_view.blank_beat)
            beat_view.is_filled = False
        beat_frame.start_pos_view.setScene(beat_frame.start_pos_view.blank_beat)
        beat_frame.start_pos_view.is_filled = False
        beat_frame.selection_overlay.deselect_beat()
        beat_frame.sequence_widget.current_word_label.update_current_word_label_from_beats()

    def _collect_widgets(self):
        beats = self.beat_frame.beats
        pictograph_items = self._get_GE_pictograph_items()
        adjustment_panel_items = self._get_adjustment_panel_items()
        widgets = (
            [
                self.sequence_widget.current_word_label,
                self.sequence_widget.difficulty_label,
                self.beat_frame.start_pos_view,
                self.beat_frame.selection_overlay,
            ]
            + beats
            + pictograph_items
            + adjustment_panel_items
        )
        return [widget for widget in widgets if widget]

    def _get_GE_pictograph_items(self):
        beat_frame = self.sequence_widget.beat_frame
        GE_pictograph = (
            beat_frame.sequence_widget.graph_editor.pictograph_container.GE_pictograph_view.pictograph
        )
        arrows: dict = GE_pictograph.arrows
        props: dict = GE_pictograph.props
        tka_glyph = GE_pictograph.tka_glyph
        tka_glyph_parts = [
            tka_glyph.letter_handler.letter_item,
            tka_glyph.dash_handler.dash_item,
            tka_glyph.dot_handler.same_dot_item,
            tka_glyph.dot_handler.opp_dot_item,
        ]
        start_to_end_pos_glyph = GE_pictograph.start_to_end_pos_glyph
        start_to_end_pos_glyph_parts = [
            start_to_end_pos_glyph.start_glyph,
            start_to_end_pos_glyph.end_glyph,
            start_to_end_pos_glyph.arrow_glyph,
        ]
        GE_glyphs = (
            [
                GE_pictograph.vtg_glyph,
                GE_pictograph.elemental_glyph,
                GE_pictograph.number_manager.beat_number_item,
                GE_pictograph.start_text_item,
            ]
            + tka_glyph_parts
            + start_to_end_pos_glyph_parts
        )

        props_list = [prop for prop in props.values()]
        arrows_list = [arrow for arrow in arrows.values()]
        pictograph_items = props_list + arrows_list + GE_glyphs
        return pictograph_items

    def _get_adjustment_panel_items(self):
        adjustment_panel = self.sequence_widget.graph_editor.adjustment_panel
        adjustment_panel_items = [
            adjustment_panel.blue_turns_box.turns_widget,
            adjustment_panel.red_turns_box.turns_widget,
            adjustment_panel.blue_turns_box.header,
            adjustment_panel.red_turns_box.header,
            adjustment_panel.blue_ori_picker.header,
            adjustment_panel.red_ori_picker.header,
            adjustment_panel.blue_ori_picker.ori_picker_widget,
            adjustment_panel.red_ori_picker.ori_picker_widget,
        ]
        return adjustment_panel_items

    def _show_no_beat_selected_message(self) -> None:
        self.sequence_widget.indicator_label.show_message(self.message)

    def _show_clear_indicator(self, show_indicator: bool) -> None:
        if show_indicator:
            self.sequence_widget.indicator_label.show_message("Sequence cleared")

    def _configure_beat_frame(self) -> None:
        if self.settings_manager.global_settings.get_grow_sequence():
            self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(0)
