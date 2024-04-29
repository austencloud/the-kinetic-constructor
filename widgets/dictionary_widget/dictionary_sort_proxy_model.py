from typing import TYPE_CHECKING
from PyQt6.QtCore import QSortFilterProxyModel, QModelIndex

if TYPE_CHECKING:
    from widgets.dictionary.dictionary_widget import DictionaryWidget


class DictionarySortProxyModel(QSortFilterProxyModel):
    def __init__(self, dictionary: "DictionaryWidget") -> None:
        super().__init__(dictionary)
        self.dictionary = dictionary
        self._lengthSortingEnabled = False
        self.visibility_settings = {}

    @property
    def lengthSortingEnabled(self) -> bool:
        return self._lengthSortingEnabled

    @lengthSortingEnabled.setter
    def lengthSortingEnabled(self, value) -> None:
        self._lengthSortingEnabled = value
        self.invalidate()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        self.sort_manager = self.dictionary.sort_manager
        self.source_model = self.dictionary.words_tree.model
        if not self.visibility_settings:
            return True

        index = self.source_model.index(source_row, 0, source_parent)
        filename = self.source_model.fileName(index)
        word_length = self.sort_manager.compute_display_length(filename)

        return self.visibility_settings.get(str(word_length), False)

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        if self.lengthSortingEnabled:
            leftData = self.source_model.fileName(left)
            rightData = self.source_model.fileName(right)
            leftLength = self.sort_manager.compute_display_length(leftData)
            rightLength = self.sort_manager.compute_display_length(rightData)
            return leftLength < rightLength
        else:
            return super().lessThan(left, right)
