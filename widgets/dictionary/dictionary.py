import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QTreeView,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QDragEnterEvent, QDropEvent
from Enums.letters import Letter, LetterConditions
from widgets.dictionary.dictionary_sequence_populator import DictionarySequencePopulator
from widgets.dictionary.dictionary_sort_manager import DictionarySortManager
from .dictionary_favorites_manager import DictionaryFavoritesTree
from .dictionary_search_sort_bar import DictionarySearchSortBar
from .dictionary_sequence_length_manager import DictionarySortByLengthHandler
from .dictionary_words_tree import DictionaryWordsTree

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

        self.layout: QVBoxLayout = QVBoxLayout(self)
        tree_layout = QHBoxLayout()
        self.setup_length_filter_buttons()
        self.search_sort_bar.setup_ui(self.layout)
        self.words_tree.setup_ui(self.layout)
        self.favorites_tree.setup_ui(tree_layout)
        self.setup_preview_area(tree_layout)
        self.setLayout(self.layout)
        self.sort_manager.sort_sequences("Length")

    def setup_length_filter_buttons(self):
        self.length_buttons_layout = QHBoxLayout()
        word_lengths = [2, 3, 4, 5, 6, 7, 8]
        visibility_settings = (
            self.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        for length in word_lengths:
            button = QPushButton(f"{length} letters")
            button.setCheckable(True)
            button.setChecked(visibility_settings.get(length, False))
            button.toggled.connect(
                lambda checked, length=length: self.toggle_word_length_visibility(
                    length, checked
                )
            )
            self.length_buttons_layout.addWidget(button)

        self.layout.addLayout(self.length_buttons_layout)

    def toggle_word_length_visibility(self, length, visible):
        visibility_settings = (
            self.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        visibility_settings[str(length)] = visible
        self.main_widget.main_window.settings_manager.set_word_length_visibility(
            visibility_settings
        )
        self.sort_manager.filter_sequences_by_length()

    def filter_sequences(self, text: str) -> None:
        search_text = text.lower()
        for i in range(self.words_tree.model.rowCount()):
            item = self.words_tree.model.item(i)
            file_name = item.text().lower()
            item.setHidden(search_text not in file_name)

    def sort_sequences_by_start_position(self) -> None:
        sequences = []
        for item in self.words_tree.extract_items(self.words_tree.model):
            file_name = item.text().replace(".json", "")
            start_letter_enum = self.get_starting_position_from_sequence_name(file_name)
            sequences.append((start_letter_enum, file_name, item))
        sequences.sort(key=lambda x: (x[0].name, x[1]))
        self.words_tree.model.clear()
        for _, name, item in sequences:
            self.words_tree.model.appendRow(item)

    @staticmethod
    def get_starting_position_from_sequence_name(name: str) -> Letter:
        for letter in Letter:
            if (
                name.startswith(letter.value)
                and letter
                in LetterConditions.ALPHA_STARTING.value
                + LetterConditions.BETA_STARTING.value
                + LetterConditions.GAMMA_STARTING.value
            ):
                return letter
        return Letter.A

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


from PyQt6.QtCore import Qt
