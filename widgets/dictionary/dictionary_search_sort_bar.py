from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QComboBox,
)

if TYPE_CHECKING:
    from widgets.dictionary.dictionary_widget import DictionaryWidget


class DictionarySearchSortBar:
    def __init__(self, dictionary: "DictionaryWidget") -> None:
        self.dictionary = dictionary
        self.search_bar = QLineEdit()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name", "Length", "Start Position"])
        self.sort_combo.currentTextChanged.connect(
            self.dictionary.sort_manager.sort_sequences
        )

    def setup_ui(self, layout: QVBoxLayout) -> None:
        search_layout = QHBoxLayout()
        self.search_bar.setPlaceholderText("Search sequences...")
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(QLabel("Sort by:"))
        search_layout.addWidget(self.sort_combo)
        layout.addLayout(search_layout)
