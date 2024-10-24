# sequence_dictionary_browser.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
import json

from main_window.main_widget.choreography_tab_widget.draggable_sequence_list_widget import (
    DraggableSequenceListWidget,
)

if TYPE_CHECKING:
    from .choreography_tab_widget.choreography_tab_widget import ChoreographyTabWidget
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView


class SequenceDictionaryBrowser(QWidget):
    def __init__(self, choreography_tab: "ChoreographyTabWidget") -> None:
        super().__init__(choreography_tab)
        self.choreography_tab = choreography_tab

        self._setup_components()
        self._setup_layout()
        self.populate_dictionary()

    def _setup_components(self):
        self.sequence_list = DraggableSequenceListWidget(self)

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.sequence_list)
        self.setLayout(layout)

    def populate_dictionary(self):
        # Load sequences from the dictionary
        sequences = (
            self.choreography_tab.main_widget.dictionary_widget.browser.get_all_sequences()
        )
        for sequence in sequences:
            item = QListWidgetItem(sequence[0])
            item.setData(Qt.ItemDataRole.UserRole, sequence)
            self.sequence_list.addItem(item)

    def resize_browser(self):
        # Adjust size based on parent widget size
        pass
