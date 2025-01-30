from typing import TYPE_CHECKING
from utilities.reversal_detector import (
    ReversalDetector,
)
from utilities.word_simplifier import WordSimplifier

if TYPE_CHECKING:
    from .sequence_beat_frame import SequenceBeatFrame


class BeatFramePopulator:
    loading_text = "Loading sequence..."

    def __init__(self, beat_frame: "SequenceBeatFrame"):
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
        print(f"current_sequence_json = {current_sequence_json}")
        indicator_label = self.sequence_widget.indicator_label
        indicator_label.show_message(self.loading_text)
        self.json_manager.loader_saver.clear_current_sequence_file()
        self.construct_tab = self.main_widget.construct_tab

        if not self.current_sequence_json:
            return

        # self.beat_frame.deletion_manager.delete_start_pos()
        self.beat_frame.updater.reset_beat_frame()
        self._set_start_position()
        self._update_sequence_layout()
        self._update_sequence_word()
        self._update_difficulty_level()
        self._populate_beats(select_beat=False)
        self._finalize_sequence()
        self.beat_frame.selection_overlay.select_beat(
            self.beat_frame.get.last_filled_beat()
        )
        indicator_label.show_message(
            f"{self.current_word} loaded successfully! Ready to edit."
        )

    def _set_start_position(self):
        start_pos_picker = self.construct_tab.start_pos_picker
        start_pos_beat = start_pos_picker.convert_current_sequence_json_entry_to_start_pos_pictograph(
            self.current_sequence_json
        )
        self.json_manager.start_pos_handler.set_start_position_data(start_pos_beat)
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

    def _populate_beats(self, select_beat=True):
        for _, pictograph_data in enumerate(self.current_sequence_json[1:]):
            if pictograph_data.get("sequence_start_position"):
                continue
            if pictograph_data.get("is_placeholder", False):
                continue
            else:
                reversal_info = ReversalDetector.detect_reversal(
                    self.current_sequence_json, pictograph_data
                )
                self.sequence_widget.beat_frame.beat_factory.create_new_beat_and_add_to_sequence(
                    pictograph_data,
                    override_grow_sequence=True,
                    update_word=False,
                    update_level=False,
                    reversal_info=reversal_info,
                    select_beat=select_beat,
                )

    def _finalize_sequence(self):
        last_beat = self.sequence_widget.beat_frame.get.last_filled_beat().beat
        self.construct_tab.last_beat = last_beat
        self.construct_tab.transition_to_option_picker()
        self.construct_tab.option_picker.updater.update_options()
        self.selection_overlay.select_beat(self.beat_frame.get.last_filled_beat())
        self.selection_overlay.update_overlay_position()

    def modify_layout_for_chosen_number_of_beats(self, beat_count):
        self.beat_frame.layout_manager.configure_beat_frame(
            beat_count, override_grow_sequence=True
        )
