import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QTreeView, QHBoxLayout
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QDragEnterEvent, QDropEvent
from Enums.letters import Letter, LetterConditions
from widgets.library.library_sequence_populator import LibrarySequencePopulator
from .library_favorites_manager import LibraryFavoritesTree
from .library_search_sort_bar import LibrarySearchSortBar
from .library_sequence_length_manager import LibrarySequenceLengthManager
from .library_words_tree import LibraryWordsTree

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Library(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.setup_ui()

    def _init_references(self):
        self.json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.start_pos_view = self.main_widget.sequence_widget.beat_frame.start_pos_view
        self.start_pos_manager = (
            self.main_widget.main_tab_widget.sequence_builder.start_pos_picker.start_pos_manager
        )
        self.sequence_widget = self.main_widget.sequence_widget
        self.sequence_builder = self.main_widget.main_tab_widget.sequence_builder

    def setup_ui(self) -> None:
        self.search_sort_bar = LibrarySearchSortBar(self)
        self.favorites_tree = LibraryFavoritesTree(self)
        self.words_tree = LibraryWordsTree(self)
        self.sequence_length_manager = LibrarySequenceLengthManager(self)
        self.sequence_populator = LibrarySequencePopulator(self)

        main_layout = QVBoxLayout(self)
        tree_layout = QHBoxLayout()
        self.search_sort_bar.setup_ui(main_layout)
        self.words_tree.setup_ui(main_layout)
        self.favorites_tree.setup_ui(tree_layout)
        self.setup_preview_area(tree_layout)
        self.setLayout(main_layout)

    def filter_sequences(self, text: str) -> None:
        search_text = text.lower()
        for i in range(self.words_tree.model.rowCount()):
            item = self.words_tree.model.item(i)
            file_name = item.text().lower()
            item.setHidden(search_text not in file_name)

    def sort_sequences(self, criteria: str) -> None:
        if criteria == "Name":
            self.words_tree.proxy_model.sort(0)
            self.words_tree.proxy_model.lengthSortingEnabled = False
        elif criteria == "Length":
            self.words_tree.proxy_model.lengthSortingEnabled = True
            self.words_tree.proxy_model.invalidate()

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

    def on_favorite_double_clicked(self, index: QModelIndex) -> None:
        item = self.favorites_tree.favorites_model.itemFromIndex(index)
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.load_sequence_from_file(file_path)

    def dragEnterEvent(self, event: "QDragEnterEvent") -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: "QDropEvent") -> None:
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".json"):
                self.add_to_favorites(file_path)

    def add_to_favorites(self, file_path: str) -> None:
        file_name = os.path.basename(file_path)
        item = QStandardItem(file_name)
        item.setData(file_path, Qt.ItemDataRole.UserRole)
        self.favorites_tree.favorites_model.appendRow(item)
        self.favorites_tree.save_favorites()

    def sort_favorites(self, column: int) -> None:
        currentOrder = self.favorites_tree.favorites_model.sortOrder()
        newOrder = (
            Qt.SortOrder.DescendingOrder
            if currentOrder == Qt.SortOrder.AscendingOrder
            else Qt.SortOrder.AscendingOrder
        )
        self.favorites_tree.favorites_model.sort(column, newOrder)

    def resize_library(self) -> None:
        self.words_tree.resize_library_words_tree()
