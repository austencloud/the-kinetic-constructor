import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox


if TYPE_CHECKING:
    from widgets.dictionary.dictionary_widget import DictionaryWidget


class DictionarySequencePopulator:
    def __init__(self, dictionary: "DictionaryWidget"):
        self.dictionary = dictionary
        self.main_widget = dictionary.main_widget
        self.initialized = False

    def _init_references(self) -> None:
        self.json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.start_pos_view = (
            self.main_widget.top_builder_widget.SW.beat_frame.start_pos_view
        )
        self.start_pos_manager = (
            self.main_widget.top_builder_widget.builder_toolbar.sequence_builder.start_pos_picker.start_pos_manager
        )
        self.SW = self.main_widget.top_builder_widget.SW
        self.sequence_builder = (
            self.main_widget.top_builder_widget.builder_toolbar.sequence_builder
        )
        self.initialized = True

    def load_sequence_from_file(self, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sequence_data = json.load(file)
            self.populate_sequence(sequence_data)
        except Exception as e:
            QMessageBox.critical(
                self.main_widget, "Error", f"Failed to load sequence: {str(e)}"
            )

    def populate_sequence(self, sequence_data: list[dict[str, str]]) -> None:
        if not self.initialized:
            self._init_references()
        if not sequence_data:
            return
        self.SW.button_frame.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )
        start_pos_beat = self.start_pos_manager._convert_current_sequence_json_entry_to_start_pos_pictograph(
            sequence_data
        )
        self.json_handler.set_start_position_data(start_pos_beat)
        self.start_pos_view.set_start_pos(start_pos_beat)
        for pictograph_dict in sequence_data:
            if pictograph_dict.get("sequence_start_position"):
                continue
            self.SW.populate_sequence(pictograph_dict)

        last_beat = self.SW.beat_frame.get_last_filled_beat().beat
        self.sequence_builder.current_pictograph = last_beat
        last_beat.view.selection_manager.select_beat(last_beat.view)

        if self.sequence_builder.start_pos_picker.isVisible():
            self.sequence_builder.transition_to_sequence_building()
        sequence = self.json_handler.load_current_sequence_json()

        self.sequence_builder.option_picker.resize_option_picker()
        scroll_area = self.sequence_builder.option_picker.scroll_area
        scroll_area.remove_irrelevant_pictographs()
        scroll_area.add_and_display_relevant_pictographs(
            self.sequence_builder.option_picker.option_manager.get_next_options(
                sequence
            )
        )
