# sequence_dictionary_browser.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidgetItem
from PyQt6.QtCore import Qt

from main_window.main_widget.write_tab.draggable_sequence import DraggableSequence


if TYPE_CHECKING:
    from main_window.main_widget.write_tab.write_tab import WriteTab


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
        sequences = (
            self.write_tab.main_widget.dictionary_widget.browser.get_all_sequences()
        )
        for sequence in sequences:
            item = QListWidgetItem(sequence[0])
            item.setData(Qt.ItemDataRole.UserRole, sequence)
            self.sequence_list.addItem(item)

    def resize_browser(self):
        pass
