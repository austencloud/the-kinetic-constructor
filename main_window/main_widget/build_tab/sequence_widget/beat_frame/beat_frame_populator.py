from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from main_window.main_widget.build_tab.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)
from utilities.word_simplifier import WordSimplifier

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
        self.current_sequence_json = []  # Initialize the instance variable

    def populate_beat_frame_from_json(
        self, current_sequence_json: list[dict[str, str]]
    ) -> None:
        self.current_sequence_json = current_sequence_json  # Store the sequence JSON
        indicator_label = self.sequence_widget.indicator_label
        indicator_label.show_message("Loading sequence...")

        self.manual_builder = self.main_widget.build_tab.sequence_constructor

        if not self.current_sequence_json:
            return

        self.beat_frame.deletion_manager.delete_all_beats()
        self._set_start_position()
        self._update_sequence_layout()
        self._update_sequence_word()
        self._update_difficulty_level()
        self._populate_beats()
        self._finalize_sequence()

        self.manual_builder.option_picker.update_option_picker()
        indicator_label.show_message(
            f"{self.current_word} loaded successfully! Ready to edit."
        )

    def _set_start_position(self):
        start_pos_picker = self.manual_builder.start_pos_picker
        start_pos_beat = start_pos_picker.convert_current_sequence_json_entry_to_start_pos_pictograph(
            self.current_sequence_json
        )
        self.json_manager.start_position_handler.set_start_position_data(start_pos_beat)
        # QApplication.processEvents()
        self.start_pos_view.set_start_pos(start_pos_beat)

    def _update_sequence_layout(self):
        length = len(self.current_sequence_json) - 2
        self.modify_layout_for_chosen_number_of_beats(length)

    def _update_difficulty_level(self):
        if len(self.current_sequence_json) > 2:
            self.sequence_widget.difficulty_label.update_difficulty_label()
        else:
            self.sequence_widget.difficulty_label.set_difficulty_level("")

    def _update_sequence_word(self):
        self.current_word = "".join(
            [
                beat["letter"]
                for beat in self.current_sequence_json[2:]
                if "letter" in beat
            ]
        )
        self.current_word = WordSimplifier.simplify_repeated_word(self.current_word)
        self.sequence_widget.current_word_label.set_current_word(self.current_word)

    def _populate_beats(self):
        for _, pictograph_dict in enumerate(self.current_sequence_json[1:]):
            if pictograph_dict.get("sequence_start_position"):
                continue
            if pictograph_dict.get("is_placeholder", False):
                continue
            else:
                reversal_info = ReversalDetector.detect_reversal(
                    self.current_sequence_json, pictograph_dict
                )
                self.sequence_widget.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                    pictograph_dict,
                    override_grow_sequence=True,
                    update_word=False,
                    update_level=False,
                    reversal_info=reversal_info,
                )

    def _finalize_sequence(self):
        last_beat = self.sequence_widget.beat_frame.get.last_filled_beat().beat
        self.manual_builder.last_beat = last_beat

        # Transition to sequence building if necessary
        self.manual_builder.transition_to_sequence_building()

        scroll_area = self.manual_builder.option_picker.scroll_area
        scroll_area.hide_all_pictographs()

        # Retrieve filters from settings
        filters = (
            self.main_widget.settings_manager.builder_settings.manual_builder.get_filters()
        )

        next_options = self.manual_builder.option_picker.option_getter.get_next_options(
            self.current_sequence_json, filters
        )

        scroll_area.add_and_display_relevant_pictographs(next_options)
        self.selection_overlay.select_beat(self.beat_frame.get.last_filled_beat())
        self.selection_overlay.update_overlay_position()

    def _add_placeholder_beat(self, pictograph_dict: dict) -> None:
        """
        Create and add a placeholder beat to the sequence.
        """
        self.json_manager.updater.add_placeholder_entry_to_current_sequence(
            pictograph_dict["beat"], pictograph_dict["parent_beat"]
        )

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )
