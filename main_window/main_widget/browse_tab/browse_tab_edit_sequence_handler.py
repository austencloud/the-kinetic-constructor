from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMessageBox

if TYPE_CHECKING:
    from .browse_tab import BrowseTab


class BrowseTabEditSequenceHandler:
    def __init__(self, browse_tab: "BrowseTab"):
        self.browse_tab = browse_tab

    def load_sequence_from_json(self, metadata: str) -> None:
        populator = self.browse_tab.main_widget.sequence_widget.beat_frame.populator
        if metadata:
            populator.populate_beat_frame_from_json(metadata["sequence"])
        else:
            QMessageBox.warning(
                self.browse_tab.main_widget,
                "Error",
                "No sequence metadata found in the thumbnail.",
            )
