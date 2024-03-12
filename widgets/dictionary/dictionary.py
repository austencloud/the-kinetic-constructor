import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QDragEnterEvent, QDropEvent
from Enums.letters import Letter, LetterConditions
from widgets.dictionary.dictionary_sequence_populator import DictionarySequencePopulator
from widgets.dictionary.dictionary_sort_manager import DictionarySortManager
from widgets.dictionary.library_word_length_selector_widget import LibraryWordLengthSelectorWidget
from .dictionary_favorites_manager import DictionaryFavoritesTree
from .dictionary_search_sort_bar import DictionarySearchSortBar
from .dictionary_sequence_length_manager import DictionarySortByLengthHandler
from .dictionary_words_tree import DictionaryWordsTree

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QTreeView,
    QHBoxLayout,
    QPushButton,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Dictionary(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setup_ui()

    def setup_ui(self) -> None:
        self.words_tree = DictionaryWordsTree(self)
        self.sort_manager = DictionarySortManager(self) 
        self.search_sort_bar = DictionarySearchSortBar(self)
        self.favorites_tree = DictionaryFavoritesTree(self)
        self.sequence_length_manager = DictionarySortByLengthHandler(self)
        self.sequence_populator = DictionarySequencePopulator(self)
        self.word_length_selector = LibraryWordLengthSelectorWidget(self)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        tree_layout = QHBoxLayout()
        self.search_sort_bar.setup_ui(self.layout)
        self.words_tree.setup_ui(self.layout)
        self.favorites_tree.setup_ui(tree_layout)
        self.setup_preview_area(tree_layout)
        self.layout.addLayout(tree_layout)
        self.layout.addWidget(self.word_length_selector)
        self.setLayout(self.layout)
        self.sort_manager.sort_sequences("Length")

    def setup_preview_area(self, layout: QVBoxLayout) -> None:
        self.preview_area = QWidget()
        self.preview_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.preview_area)

    def on_double_clicked(self, index: QModelIndex) -> None:
        # Map the proxy index to source index before getting the file path
        source_index = self.words_tree.proxy_model.mapToSource(index)
        file_path = self.words_tree.model.filePath(source_index)

        if file_path.endswith(".json"):
            self.sequence_populator.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def dragEnterEvent(self, event: "QDragEnterEvent") -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: "QDropEvent") -> None:
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".json"):
                self.add_to_favorites(file_path)

    def resize_dictionary(self) -> None:
        self.words_tree.resize_dictionary_words_tree()

