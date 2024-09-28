from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .sequence_widget_beat_frame import SequenceWidgetBeatFrame


class BeatFramePopulator:
    def __init__(self, beat_frame: "SequenceWidgetBeatFrame"):
        self.beat_frame = beat_frame
        self.main_widget = beat_frame.main_widget
        self.sequence_widget = beat_frame.sequence_widget
        self.start_pos_view = beat_frame.start_pos_view
        self.selection_overlay = beat_frame.selection_overlay
        self.json_manager = beat_frame.json_manager

    def populate_beat_frame_from_json(
        self, current_sequence_json: list[dict[str, str]]
    ) -> None:
        self.start_pos_manager = (
            self.main_widget.top_builder_widget.sequence_builder.manual_builder.start_pos_picker.start_pos_manager
        )
        self.sequence_builder = self.main_widget.top_builder_widget.sequence_builder
        if not current_sequence_json:
            return
        self.sequence_widget.sequence_clearer.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )
        start_pos_beat = self.start_pos_manager.convert_current_sequence_json_entry_to_start_pos_pictograph(
            current_sequence_json
        )
        self.json_manager.start_position_handler.set_start_position_data(start_pos_beat)
        self.start_pos_view.set_start_pos(start_pos_beat)
        for pictograph_dict in current_sequence_json[1:]:
            if pictograph_dict.get("sequence_start_position"):
                continue
            self.sequence_widget.create_new_beat_and_add_to_sequence(pictograph_dict)
        self.sequence_widget.update_current_word()
        if len(current_sequence_json) > 2:
            self.sequence_widget.update_difficulty_label()
        else:
            self.sequence_widget.difficulty_label.set_difficulty_level("")
        last_beat = self.sequence_widget.beat_frame.get.last_filled_beat().beat
        self.sequence_builder.manual_builder.last_beat = last_beat

        if self.sequence_builder.manual_builder.start_pos_picker.isVisible():
            self.sequence_builder.manual_builder.transition_to_sequence_building()

        scroll_area = self.sequence_builder.manual_builder.option_picker.scroll_area
        scroll_area.remove_irrelevant_pictographs()
        next_options = self.sequence_builder.manual_builder.option_picker.option_getter.get_next_options(
            current_sequence_json
        )

        scroll_area.add_and_display_relevant_pictographs(next_options)
        self.selection_overlay.select_beat(self.beat_frame.get.last_filled_beat())
        self.selection_overlay.update_overlay_position()
