from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QComboBox,
)

if TYPE_CHECKING:
    from widgets.library.library import Library


class LibrarySearchSortBar:
    def __init__(self, library: "Library") -> None:
        self.library = library
        self.search_bar = QLineEdit()
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name", "Length", "Start Position"])
        self.sort_combo.currentTextChanged.connect(self.library.sort_sequences)

    def setup_ui(self, layout: QVBoxLayout) -> None:
        search_layout = QHBoxLayout()
        self.search_bar.setPlaceholderText("Search sequences...")
        self.search_bar.textChanged.connect(self.library.filter_sequences)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_bar)
        search_layout.addWidget(QLabel("Sort by:"))
        search_layout.addWidget(self.sort_combo)
        layout.addLayout(search_layout)
