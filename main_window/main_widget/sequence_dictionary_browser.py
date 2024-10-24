# sequence_dictionary_browser.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
import json

from main_window.main_widget.write_widget.draggable_sequence import (
    DraggableSequence,
)

if TYPE_CHECKING:
    from .write_widget.write_tab import WriteTab
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView


class SequenceDictionaryBrowser(QWidget):
    def __init__(self, write_tab: "WriteTab") -> None:
        super().__init__(write_tab)
        self.write_tab = write_tab

        self._setup_components()
        self._setup_layout()
        self.populate_dictionary()

    def _setup_components(self):
        self.sequence_list = DraggableSequence(self)

    def _setup_layout(self):
        layout = QVBoxLayout(self)
        layout.addWidget(self.sequence_list)
        self.setLayout(layout)

    def populate_dictionary(self):
        # Load sequences from the dictionary
        sequences = (
            self.write_tab.main_widget.dictionary_widget.browser.get_all_sequences()
        )
        for sequence in sequences:
            item = QListWidgetItem(sequence[0])
            item.setData(Qt.ItemDataRole.UserRole, sequence)
            self.sequence_list.addItem(item)

    def resize_browser(self):
        # Adjust size based on parent widget size
        pass
