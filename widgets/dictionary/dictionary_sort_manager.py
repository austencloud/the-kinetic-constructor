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
from .dictionary_favorites_manager import DictionaryFavoritesTree
from .dictionary_search_sort_bar import DictionarySearchSortBar
from .dictionary_sequence_length_manager import DictionarySortByLengthHandler
from .dictionary_words_tree import DictionaryWordsTree

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary
    

class DictionarySortManager:
    def __init__(self, dictionary: "Dictionary"):
        self.dictionary = dictionary
        # Assumes proxy_model has visibility_settings and lengthSortingEnabled
        self.proxy_model = self.dictionary.words_tree.proxy_model

    def sort_sequences(self, criteria):
        if criteria == "Name":
            self.proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.proxy_model.setDynamicSortFilter(True)
            self.proxy_model.lengthSortingEnabled = False
            self.proxy_model.setSortRole(Qt.ItemDataRole.DisplayRole)
        elif criteria == "Length":
            self.proxy_model.lengthSortingEnabled = True
        elif criteria == "Date":
            pass
        self.proxy_model.invalidate()
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

    def sort_favorites(self, column: int) -> None:
        currentOrder = self.dictionary.favorites_tree.favorites_model.sortOrder()
        newOrder = (
            Qt.SortOrder.DescendingOrder
            if currentOrder == Qt.SortOrder.AscendingOrder
            else Qt.SortOrder.AscendingOrder
        )
        self.dictionary.favorites_tree.favorites_model.sort(column, newOrder)


    def filter_sequences_by_length(self):
        visibility_settings = (
            self.dictionary.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        for i in range(self.proxy_model.rowCount()):
            index = self.proxy_model.index(i, 0)
            sequence_name = self.proxy_model.data(index)
            sequence_length = self.compute_display_length(sequence_name)
            should_be_visible = visibility_settings.get(str(sequence_length), False)
            self.proxy_model.setData(
                index, not should_be_visible, Qt.ItemDataRole.UserRole + 1
            )

    @staticmethod
    def compute_display_length(name: str) -> int:
        count = 0
        skip_next = False
        for i, char in enumerate(name):
            if skip_next:
                skip_next = False
                continue
            if char == "-" and i + 1 < len(name):
                count += 1
                skip_next = True
            else:
                count += 1
        return count
