from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from main_window.main_widget.browse_tab.browse_tab import (
        BrowseTab,
    )


class BrowseTabEditSequenceHandler:
    def __init__(self, dictionary: "BrowseTab"):
        self.dictionary = dictionary
        self.main_widget = dictionary.main_widget
        self.initialized = False
        self._init_references()

    def _init_references(self) -> None:
        self.json_manager = self.main_widget.json_manager
        self.start_pos_view = self.main_widget.sequence_widget.beat_frame.start_pos_view

        self.sequence_widget = self.main_widget.sequence_widget
        self.beat_frame = self.sequence_widget.beat_frame
        self.initialized = True

    def load_sequence_from_json(self, metadata: str) -> None:
        if metadata:
            self.beat_frame.populator.populate_beat_frame_from_json(
                metadata["sequence"]
            )
        else:
            QMessageBox.warning(
                self.dictionary.main_widget,
                "Error",
                "No sequence metadata found in the thumbnail.",
            )
