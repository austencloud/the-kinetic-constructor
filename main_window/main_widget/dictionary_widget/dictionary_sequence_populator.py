import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_widget import (
        DictionaryWidget,
    )


class DictionarySequencePopulator:
    def __init__(self, dictionary: "DictionaryWidget"):
        self.dictionary = dictionary
        self.main_widget = dictionary.main_widget
        self.initialized = False
        self._init_references()

    def _init_references(self) -> None:
        self.json_manager = self.main_widget.json_manager
        self.start_pos_view = (
            self.main_widget.top_builder_widget.sequence_widget.beat_frame.start_pos_view
        )
        self.start_pos_manager = (
            self.main_widget.top_builder_widget.sequence_builder.manual_builder.start_pos_picker.start_pos_manager
        )
        self.sequence_widget = self.main_widget.top_builder_widget.sequence_widget
        self.sequence_builder = self.main_widget.top_builder_widget.sequence_builder
        self.beat_frame = self.sequence_widget.beat_frame
        self.initialized = True

    def load_sequence_from_file(self, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sequence_data = json.load(file)
            self.beat_frame.populator.populate_beat_frame_from_json(sequence_data)
        except Exception as e:
            QMessageBox.critical(
                self.main_widget, "Error", f"Failed to load sequence: {str(e)}"
            )

    def load_sequence_from_json(self, metadata: str) -> None:
        if metadata:
            self.beat_frame.populator.populate_beat_frame_from_json(metadata["sequence"])
        else:
            QMessageBox.warning(
                self.dictionary.main_widget,
                "Error",
                "No sequence metadata found in the thumbnail.",
            )
